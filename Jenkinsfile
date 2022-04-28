pipeline {
    agent {
        docker {
            reuseNode false
            image 'justaddcoffee/ubuntu20-python-3-8-5-dev:6'
        }
    }
    //triggers{
    //    cron('H H 1 1-12 *')
    //}
    environment {
        BUILDSTARTDATE = sh(script: "echo `date +%Y%m%d`", returnStdout: true).trim()
        S3PROJECTDIR = 'kg-ontoml' // no trailing slash

        // Distribution ID for the AWS CloudFront for this bucket
        // used solely for invalidations
        AWS_CLOUDFRONT_DISTRIBUTION_ID = 'EUVSWXZQBXCFP'

        MERGEDKGNAME_BASE = "KG-OntoML"
        MERGEDKGNAME_GENERIC = "merged-kg"
    }
    options {
        timestamps()
        disableConcurrentBuilds()
    }
    stages {
        // Very first: pause for a minute to give a chance to
        // cancel and clean the workspace before use.
        stage('Ready and clean') {
            steps {
                // Give us a minute to cancel if we want.
                sleep time: 30, unit: 'SECONDS'
            }
        }

        stage('Initialize') {
            steps {
                // print some info
                dir('./gitrepo') {
                    sh 'env > env.txt'
                    sh 'echo $BRANCH_NAME > branch.txt'
                    sh 'echo "$BRANCH_NAME"'
                    sh 'cat env.txt'
                    sh 'cat branch.txt'
                    sh "echo $BUILDSTARTDATE > dow.txt"
                    sh "echo $BUILDSTARTDATE"
                    sh "echo $MERGEDKGNAME_BASE"
                    sh "echo $MERGEDKGNAME_GENERIC"
                    sh "python3.8 --version"
                    sh "id"
                    sh "whoami" // this should be jenkinsuser
                    // if the above fails, then the docker host didn't start the docker
                    // container as a user that this image knows about. This will
                    // likely cause lots of problems (like trying to write to $HOME
                    // directory that doesn't exist, etc), so we should fail here and
                    // have the user fix this

                }
            }
        }

        stage('Build kg_ontoml') {
            steps {
                dir('./gitrepo') {
                    git(
                            url: 'https://github.com/Knowledge-Graph-Hub/kg-ontoml',
                            branch: env.BRANCH_NAME
                    )
                    sh '/usr/bin/python3.8 -m venv venv'
                    sh '. venv/bin/activate'
                    sh './venv/bin/pip install .'
                    sh './venv/bin/pip install awscli boto3 s3cmd'
                    sh './venv/bin/pip install git+https://github.com/Knowledge-Graph-Hub/NEAT.git'
                }
            }
        }

        stage('Download') {
            steps {
                dir('./gitrepo') {
                    script {
                        
                        // Verify that the project directory is defined, or it will make a mess
                        // when it uploads everything to the wrong directory
                        if (S3PROJECTDIR.replaceAll("\\s","") == '') {
                            error("Project name contains only whitespace. Will not continue.")
                        }

                        def run_py_dl = sh(
                            script: '. venv/bin/activate && python3.8 run.py download', returnStatus: true
                        )
                        if (run_py_dl == 0) {
                            if (env.BRANCH_NAME != 'master') { // upload raw to s3 if we're on correct branch
                                echo "Will not push if not on correct branch."
                            } else {
                                withCredentials([file(credentialsId: 's3cmd_kg_hub_push_configuration', variable: 'S3CMD_CFG')]) {
                                    sh '. venv/bin/activate && s3cmd -c $S3CMD_CFG --acl-public --mime-type=plain/text --cf-invalidate put -r data/raw s3://kg-hub-public-data/$S3PROJECTDIR/'
                                }
                            }
                        }  else { // 'run.py download' failed - let's try to download last good copy of raw/ from s3 to data/
                            currentBuild.result = "UNSTABLE"
                            withCredentials([file(credentialsId: 's3cmd_kg_hub_push_configuration', variable: 'S3CMD_CFG')]) {
                                sh 'rm -fr data/raw || true;'
                                sh 'mkdir -p data/raw || true'
                                sh '. venv/bin/activate && s3cmd -c $S3CMD_CFG --acl-public --mime-type=plain/text get -r s3://kg-hub-public-data/$S3PROJECTDIR/raw/ data/raw/'
                            }
                        }
                    }
                }
            }
        }

        stage('Transform') {
            steps {
                dir('./gitrepo') {
		            sh '. venv/bin/activate && env && python3.8 run.py transform'
                }
            }
        }

        stage('Merge') {
            steps {
                dir('./gitrepo') {
                    sh '. venv/bin/activate && python3.8 run.py merge -y merge.yaml'
                    sh 'cp merged_graph_stats.yaml merged_graph_stats_$BUILDSTARTDATE.yaml'
                    sh 'tar -rvfz data/merged/merged-kg.tar.gz merged_graph_stats_$BUILDSTARTDATE.yaml'
                    sh 'tar -xvzf data/merged/merged-kg.tar.gz'   
                    sh '. venv/bin/activate && python3.8 graph_prefixcats.py --input merged-kg_nodes.tsv --output merged-kg_nodes-prefixcats.tsv'
                    sh 'cp data/merged/merged-kg.tar.gz data/merged/merged-kg-prefixcats.tar.gz'
                    sh 'tar -rvfz data/merged/merged-kg-prefixcats.tar.gz merged-kg_nodes-prefixcats.tsv'
                }
            }
        }

        stage('Publish') {
            steps {
                dir('./gitrepo') {
                    script {

                        // make sure we aren't going to clobber existing data
                        withCredentials([file(credentialsId: 's3cmd_kg_hub_push_configuration', variable: 'S3CMD_CFG')]) {
                            REMOTE_BUILD_DIR_CONTENTS = sh (
                                script: '. venv/bin/activate && s3cmd -c $S3CMD_CFG ls s3://kg-hub-public-data/$S3PROJECTDIR/$BUILDSTARTDATE/',
                                returnStdout: true
                            ).trim()
                            echo "REMOTE_BUILD_DIR_CONTENTS (THIS SHOULD BE EMPTY): '${REMOTE_BUILD_DIR_CONTENTS}'"
                            if("${REMOTE_BUILD_DIR_CONTENTS}" != ''){
                                echo "Will not overwrite existing remote S3 directory: $S3PROJECTDIR/$BUILDSTARTDATE"
                                sh 'exit 1'
                            } else {
                                echo "remote directory $S3PROJECTDIR/$BUILDSTARTDATE is empty, proceeding"
                            }
                        }

                        if (env.BRANCH_NAME != 'master') {
                            echo "Will not push if not on correct branch."
                        } else {
                            withCredentials([
					            file(credentialsId: 's3cmd_kg_hub_push_configuration', variable: 'S3CMD_CFG'),
					            file(credentialsId: 'aws_kg_hub_push_json', variable: 'AWS_JSON'),
					            string(credentialsId: 'aws_kg_hub_access_key', variable: 'AWS_ACCESS_KEY_ID'),
					            string(credentialsId: 'aws_kg_hub_secret_key', variable: 'AWS_SECRET_ACCESS_KEY')]) {
                                                              
                                //
                                // make $BUILDSTARTDATE/ directory and sync to s3 bucket
                                //
                                sh 'mkdir $BUILDSTARTDATE/'
                                sh 'cp -p data/merged/${MERGEDKGNAME_BASE}.nt.gz $BUILDSTARTDATE/${MERGEDKGNAME_BASE}.nt.gz'
                                sh 'cp -p data/merged/merged-kg.tar.gz $BUILDSTARTDATE/${MERGEDKGNAME_BASE}.tar.gz'

                                // transformed data
                                sh 'rm -fr data/transformed/.gitkeep'
                                sh 'cp -pr data/transformed $BUILDSTARTDATE/'
                                sh 'cp -pr data/raw $BUILDSTARTDATE/'
                                sh 'cp Jenkinsfile $BUILDSTARTDATE/'

                                // copy that NEAT config, too
                                // but update its buildname internally first
                                sh """ sed -i '/s3_bucket_dir/ s/kg-ontoml/$S3PROJECTDIR\\/$BUILDSTARTDATE\\/graph_ml/' neat.yaml """
                                sh 'cp neat.yaml $BUILDSTARTDATE/'

                                // stats dir
                                sh 'mkdir $BUILDSTARTDATE/stats/'
                                sh 'cp -p *_stats.yaml $BUILDSTARTDATE/stats/'
				
                                // build the index, then upload to remote
                                sh '. venv/bin/activate && multi_indexer -v --directory $BUILDSTARTDATE --prefix https://kg-hub.berkeleybop.io/$S3PROJECTDIR/$BUILDSTARTDATE -x -u'

                                sh 's3cmd -c $S3CMD_CFG put -pr --acl-public --cf-invalidate $BUILDSTARTDATE s3://kg-hub-public-data/$S3PROJECTDIR/'
                                sh 's3cmd -c $S3CMD_CFG rm -r s3://kg-hub-public-data/$S3PROJECTDIR/current/'
                                sh 's3cmd -c $S3CMD_CFG put -pr --acl-public --cf-invalidate $BUILDSTARTDATE/* s3://kg-hub-public-data/$S3PROJECTDIR/current/'

                                // make index for project dir
                                sh '. venv/bin/activate && multi_indexer -v --prefix https://kg-hub.berkeleybop.io/$S3PROJECTDIR/ -b kg-hub-public-data -r $S3PROJECTDIR -x'
                                sh 's3cmd -c $S3CMD_CFG put -pr --acl-public --cf-invalidate ./index.html s3://kg-hub-public-data/$S3PROJECTDIR/'

                                // Invalidate the CDN now that the new files are up.
                                sh 'echo "[preview]" > ./awscli_config.txt && echo "cloudfront=true" >> ./awscli_config.txt'
                                sh '. venv/bin/activate && AWS_CONFIG_FILE=./awscli_config.txt python3.8 ./venv/bin/aws cloudfront create-invalidation --distribution-id $AWS_CLOUDFRONT_DISTRIBUTION_ID --paths "/*"'

                                // Should now appear at:
                                // https://kg-hub.berkeleybop.io/kg-ontoml/
                            }

                        }
                    }
                }
            }
        }

        // stage('Deploy blazegraph') {
        //     when { anyOf { branch 'master' } }
        //     steps {
        //         git([branch: 'master',
        //              credentialsId: 'justaddcoffee_github_api_token_username_pw',
        //              url: 'https://github.com/geneontology/operations.git'])

        //         dir('./ansible') {

        //             withCredentials([file(credentialsId: 'ansible-bbop-local-slave', variable: 'DEPLOY_LOCAL_IDENTITY')]) {
        //                 echo 'Push master out to public Blazegraph'

        //                 // these commands ensure that ansible's ssh command doesn't
        //                 // fail (in a very difficult-to-debug way) when it needs
        //                 // us to accept the public key of pan.lbl.gov
        //                 sh 'mkdir -p ~/.ssh/'
        //                 sh 'ssh-keyscan -H pan.lbl.gov >> ~/.ssh/known_hosts'

        //                 retry(3){
        //                     sh 'HOME=`pwd` && ansible-playbook update-kg-hub-endpoint.yaml --inventory=hosts.local-rdf-endpoint --private-key="$DEPLOY_LOCAL_IDENTITY" -e target_user=bbop --extra-vars="endpoint=internal"'
        //                 }
        //             }
        //         }

        //     }
        // }
    }

    post {
        always {
            echo 'In always'
            echo 'Cleaning workspace...'
            cleanWs()
        }
        success {
            echo 'I succeeded!'
        }
        unstable {
            echo 'I am unstable :/'
        }
        failure {
            echo 'I failed :('
        }
        changed {
            echo 'Things were different before...'
        }
    }
}
