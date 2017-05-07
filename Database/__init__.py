__all__ = ["connector","cursor","sql_utilities"]

DB_CONNECT = {'host' : '127.0.0.1', 'port' : 4444, 'user' : 'user', 'password' : 'password'}

TABLE_PROD_TV_SERIES = {
		'cMain' :  
			{
				'productID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY', 'productTitle' : 'VARCHAR(48)', 'skuNo' : 'INT', 'productType' : 'INT', 
				'productPage' : 'VARCHAR(128)', 'imageLink': 'VARCHAR(128)', 'imageFolder' : 'INT', 'format' : 'INT',
				'vidFormat' : 'INT', 'transFormat' : 'INT', 'aspectRatio' : 'INT', 'primaryAudio' : 'INT', 'discCount' : 'INT',
				'regionCode' : 'INT', 'oflcRating' : 'INT', 'runTime' : 'INT', 'genres' : 'INT', 'actors' : 'INT',
				'distributor' : 'INT', 'releaseDate' : 'INT', 'imageLink' : 'INT'
			},
		'fk' :
			{
			'cProdType' :
				{
					'productTypeID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY', 'productType' : 'VARCHAR(16)'
				},
			'cImageFolder' : 
				{
					'imageFolderID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY', 'imageFolder' : 'VARCHAR(128)'
				},
			'cVideoFormat' : 
				{ 
					'vidFormatID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY', 'vidformat' : 'VARCHAR(16)' 
				},
			'cTransferFormat' : 
				{ 
					'transFormatID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY', 'transFormat' : 'VARCHAR(16)'
				},
			'cAspectRatio' : 
				{ 
					'aspectRatioID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY', 'aspectRatio' : 'VARCHAR(16)'
				},
			'cPrimaryAudio' : 
				{ 
					'primaryAudioID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY', 'primaryAudio' : 'VARCHAR(16)'
				},
			'cDiscCount' : 
				{ 
					'discCountID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY', 'discCount' : 'INT'
				},
			'cRegionCode' : 
				{ 
					'regionCodeID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY', 'regionCode' : 'VARCHAR(8)'
				},
			'cOflcRating' : 
				{ 
					'oflcRatingID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY', 'oflcRating' : 'VARCHAR(8)'
				},
			'cRunTime' : 
				{ 
					'runTimeID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY', 'runTime' : 'VARCHAR(12)'
				},
			'cGenres' : 
				{ 
					'genresID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY', 'genres' : 'VARCHAR(4)'
				},
			'cActors' : 
				{ 
					'actorsID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY', 'actors' : 'VARCHAR(256)'
				},
			'cDistributor' : 
				{ 
					'distributorID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY', 'distributor' : 'VARCHAR(64)'
				},
			'cReleaseDate' : 
				{ 
					'releaseDateID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY', 'releaseDate' : 'VARCHAR(24)'
				},
			'cCatalogNo' : 
				{ 
					'catalogNoID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY', 'catalogNo' : 'INT'
				},
			'cFormatNo' : 
				{ 
					'formatID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY', 'format' : 'VARCHAR(16)'
				},
			'cImageLink' : 
				{ 
					'imageLinkID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY', 'format' : 'VARCHAR(16)'
				}
			}
		}
