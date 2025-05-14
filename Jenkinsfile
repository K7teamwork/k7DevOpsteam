pipeline {
    agent any
    stages {
        stage('Setup Environment') {
            steps {
                sh '''
                # Clean previous deployment
                sudo rm -rf /var/www/static/*
                sudo rm -f /run/gunicorn.sock
                
                # Create fresh virtualenv
                python -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }
        
        stage('Collect Static Files') {
            steps {
                sh '''
                . venv/bin/activate
                cd election
                
                # Create static directory with correct permissions
                sudo mkdir -p /var/www/static
                sudo chown -R jenkins:www-data /var/www/static
                sudo chmod -R 775 /var/www/static
                
                # Collect static files
                python manage.py collectstatic --noinput --clear
                
                # Final permission fix
                sudo chown -R www-data:www-data /var/www/static
                sudo find /var/www/static -type d -exec chmod 755 {} \\;
                sudo find /var/www/static -type f -exec chmod 644 {} \\;
                '''
            }
        }
        
        stage('Deploy Gunicorn') {
            steps {
                sh '''
                . venv/bin/activate
                cd election
                
                # Create socket directory
                sudo mkdir -p /run/gunicorn
                sudo chown jenkins:www-data /run/gunicorn
                sudo chmod 775 /run/gunicorn
                
                # Start Gunicorn
                gunicorn --bind unix:/run/gunicorn.sock \
                         --workers 3 \
                         --access-logfile - \
                         --error-logfile - \
                         election.wsgi:application &
                '''
            }
        }
        
        stage('Configure Nginx') {
            steps {
                sh '''
                # Test Nginx config
                sudo nginx -t
                
                # Restart Nginx
                sudo systemctl restart nginx
                
                # Verify deployment
                sleep 5
                curl -I http://localhost/static/admin/css/base.css
                curl -I http://localhost
                '''
            }
        }
    }
}