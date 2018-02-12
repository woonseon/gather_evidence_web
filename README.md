#gather_evidence_web

For gathering web evidence

    Requirements
        Language
            python2.x
        
        Module
            apt-get install python-qt4
            pip install piexif
            pip install pytz
            pip install pymysql
       
        DB
            Server version: 5.7.21-0ubuntu0.16.04.1 (Ubuntu)
            
            CREATE DATABASE evidence;
            CREATE TABLE `evidence`.`get_evidence` ( `time` VARCHAR(255) NOT NULL , `filename` VARCHAR(255) NOT NULL , \
            `md5_hash` VARCHAR(255) NOT NULL , `sha1_hash` VARCHAR(255) NOT NULL );


    Setup
        ./setup.sh


    Usage
        python g_evdence.py

    
