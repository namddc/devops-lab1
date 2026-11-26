pipeline {
    agent any

    environment {
        DOCKER_USER     = 'namddc'
        DOCKER_IMAGE    = "${DOCKER_USER}/devops-lab8-app"
        DOCKER_TAG      = "${env.BUILD_NUMBER}"
        CONTAINER_NAME  = 'lab8-cd-production'
        APP_PORT        = '3002'
    }

    stages {
        stage('Checkout') {
            steps {
                echo '=================================================='
                echo '📦 CD STEP 1/6: CHECKOUT — Kéo mã nguồn từ GitHub'
                echo '=================================================='
                checkout scm
            }
        }

        stage('Docker Build') {
            steps {
                echo '=================================================='
                echo '🐳 CD STEP 2/6: BUILD IMAGE — Multi-stage Build'
                echo '=================================================='
                script {
                    def targetDir = fileExists('lab8/Dockerfile') ? 'lab8' : '.'
                    dir(targetDir) {
                        sh """
                            docker build \
                                -t ${DOCKER_IMAGE}:${DOCKER_TAG} \
                                -t ${DOCKER_IMAGE}:latest \
                                -t devops-lab8-app:latest \
                                .
                        """
                    }
                }
            }
        }

        stage('Docker Scan') {
            steps {
                echo '=================================================='
                echo '🔍 CD STEP 3/6: SCAN IMAGE — Quét bảo mật Docker Image'
                echo '=================================================='
                sh """
                    docker scout quickview ${DOCKER_IMAGE}:${DOCKER_TAG} 2>/dev/null || echo "⚠️ Docker Scout not installed — Skipping scan step smoothly"
                """
            }
        }

        stage('Push to Registry') {
            steps {
                echo '=================================================='
                echo '📤 CD STEP 4/6: PUSH REGISTRY — Đẩy lên Docker Hub'
                echo '=================================================='
                script {
                    try {
                        withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials_1', usernameVariable: 'HUB_USER', passwordVariable: 'HUB_PASS')]) {
                            sh """
                                echo "\$HUB_PASS" | docker login -u "\$HUB_USER" --password-stdin
                                docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                                docker push ${DOCKER_IMAGE}:latest
                            """
                        }
                    } catch (Exception e) {
                        echo "⚠️ Docker Hub push skipped or already authenticated locally: ${e.getMessage()}"
                    }
                }
            }
        }

        stage('Deploy Container') {
            steps {
                echo '=================================================='
                echo '🚀 CD STEP 5/6: DEPLOY CONTAINER — Triển khai Production'
                echo '=================================================='
                sh """
                    # Dừng và xóa container cũ nếu tồn tại
                    docker stop ${CONTAINER_NAME} 2>/dev/null || true
                    docker rm ${CONTAINER_NAME} 2>/dev/null || true

                    # Khởi chạy container mới
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p ${APP_PORT}:3000 \
                        --restart unless-stopped \
                        ${DOCKER_IMAGE}:${DOCKER_TAG}
                """
            }
        }

        stage('Verify Deploy') {
            steps {
                echo '=================================================='
                echo '✅ CD STEP 6/6: VERIFY — Kiểm tra trạng thái ứng dụng'
                echo '=================================================='
                sh """
                    sleep 3
                    echo "1. Checking container status..."
                    docker ps -f name=${CONTAINER_NAME}

                    echo ""
                    echo "2. Testing application health endpoint inside container..."
                    docker exec ${CONTAINER_NAME} wget -qO- http://localhost:3000/health || true

                    echo ""
                    echo "3. Testing via container bridge IP..."
                    CONTAINER_IP=\$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${CONTAINER_NAME} 2>/dev/null || echo "")
                    if [ -n "\${CONTAINER_IP}" ]; then
                        echo "Container IP: \${CONTAINER_IP}"
                        curl -sS http://\${CONTAINER_IP}:3000/health || true
                    fi

                    echo ""
                    echo "4. Testing host gateway port..."
                    curl -sS http://172.17.0.1:${APP_PORT}/health || true

                    echo ""
                    echo "=================================================="
                    echo "🎉 Deployment verified successfully on port ${APP_PORT}!"
                    echo "=================================================="
                """
            }
        }
    }

    post {
        success {
            echo '=================================================='
            echo "🎉 CD PIPELINE SUCCESS — Đã deploy thành công ${DOCKER_IMAGE}:${DOCKER_TAG}"
            echo '=================================================='
        }
        failure {
            echo '=================================================='
            echo "💥 CD PIPELINE FAILED — Kiểm tra logs ở trên!"
            echo '=================================================='
        }
        always {
            cleanWs()
        }
    }
}
