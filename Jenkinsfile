pipeline {

    agent {
        node {
            label 'slave_node1'
        }
    }
    environment {
        PATH = "/home/ec2-user/miniforge3/bin:$PATH"
        }
    stages {
        
        stage('Code Checkout') {
            steps {
             checkout scm
            }
        }

        // stage('Python linting and Formatting') {
        //     steps{
        //         // activate virtual environment
        //         sh '''#!/usr/bin/env bash
        //         export PATH=/home/ec2-user/miniforge3/bin:$PATH # modify this path 
        //         eval "$(conda shell.bash hook)"
        //         /home/ec2-user/miniforge3/bin/conda env remove --name pre-ml-env -y
        //         /home/ec2-user/miniforge3/bin/conda activate 
        //         /home/ec2-user/miniforge3/bin/conda env create -n pre-ml-env -f conda-environment.yml -y
        //         /home/ec2-user/miniforge3/bin/conda activate pre-ml-env
        //         echo "Using python:" $(which python)
        //         pip install -r requirements.dev.txt
        //         ./scripts/lint
        //         /home/ec2-user/miniforge3/bin/conda deactivate
        //         /home/ec2-user/miniforge3/bin/conda env remove --name pre-ml-env -y
        //         /home/ec2-user/miniforge3/bin/conda deactivate
        //         '''
        //     }
        // }

        stage('Deploying on Stage') {
             when {
                branch 'stage'
            }
            steps{
                sh 'mkdir -p certificates'
                sh 'cp /opt/certificates/stage/private.key $WORKSPACE/certificates/private.key'
                sh 'cp /opt/certificates/stage/public.key $WORKSPACE/certificates/public.key'
                sh 'docker build --build-arg ACCESS_TOKEN_USR --build-arg ACCESS_TOKEN_PWD -t camgateway .'
                sh 'docker tag camgateway 122974644486.dkr.ecr.us-east-2.amazonaws.com/camgateway:$BUILD_ID'
                sh 'aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 122974644486.dkr.ecr.us-east-2.amazonaws.com'
                sh 'docker push 122974644486.dkr.ecr.us-east-2.amazonaws.com/camgateway:$BUILD_ID'
                sh 'docker rmi 122974644486.dkr.ecr.us-east-2.amazonaws.com/camgateway:$BUILD_ID'
                sh 'aws eks --region us-east-1 update-kubeconfig --name chefling-stage-EKS'
                sh "sed -i 's|aws-iam-authenticator|/home/ec2-user/bin/aws-iam-authenticator|g' /home/ec2-user/.kube/config"
                sh '/home/ec2-user/bin/kubectl set image deployments/camgateway camgateway=122974644486.dkr.ecr.us-east-2.amazonaws.com/camgateway:$BUILD_ID'
                sh '/home/ec2-user/bin/kubectl get pods'
            }
        }

        stage ('Deploying on Prod'){
            when {
                branch 'prod'
            }
            steps {
                sh 'mkdir -p certificates'
                sh 'cp /opt/certificates/prod/private.key $WORKSPACE/certificates/private.key'
                sh 'cp /opt/certificates/prod/public.key $WORKSPACE/certificates/public.key'
                sh 'docker build --build-arg ACCESS_TOKEN_USR --build-arg ACCESS_TOKEN_PWD -t camgateway .'
                sh 'docker tag camgateway 122974644486.dkr.ecr.us-west-2.amazonaws.com/camgateway:$BUILD_ID'
                sh 'aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 122974644486.dkr.ecr.us-west-2.amazonaws.com'
                sh 'docker push 122974644486.dkr.ecr.us-west-2.amazonaws.com/camgateway:$BUILD_ID'
                sh 'docker rmi 122974644486.dkr.ecr.us-west-2.amazonaws.com/camgateway:$BUILD_ID'
                sh 'aws eks --region us-west-2 update-kubeconfig --name prod-eks'
                sh "sed -i 's|aws-iam-authenticator|/home/ec2-user/bin/aws-iam-authenticator|g' /home/ec2-user/.kube/config"
                sh '/home/ec2-user/bin/kubectl set image deployments/camgateway camgateway=122974644486.dkr.ecr.us-west-2.amazonaws.com/camgateway:$BUILD_ID'
                sh '/home/ec2-user/bin/kubectl get pods'
            }
        }
    } 
}
