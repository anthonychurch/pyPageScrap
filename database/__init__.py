__all__ = ["cursor","sql_utilities"]

DB_CONNECT = {'host' : '127.0.0.1', 'port' : 3306, 'user' : 'root', 'password' : 'please#101'}

DB_PROD_TV_SERIES = 'products'

IMG_DIR_BASE = 'E:\\websites\\blu_ray_store\\tv_series'

TABLE_PROD_TV_SERIES = {
		# Table name
		# 'm' prefix indicates that it is a main table that may have forign keys or constrained tables attached to it
		'table' :  
			{
			'm_products' :
				{
					# Table columns and their values
					'id' :
						{
							'productID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY'
						},
					'columns' :
						{
							'productTitle' : 'VARCHAR(256)', 'skuNo' : 'INT', 'productTypeID' : 'INT', 
							'productPage' : 'VARCHAR(256)', 'imageLink': 'VARCHAR(128)', 'thumbImageLink': 'VARCHAR(128)', 
							'distributor': 'VARCHAR(64)', 'imageName': 'VARCHAR(256)', 'retailerID': 'INT',
							'imageFolderID' : 'INT', 'vidFormatID' : 'INT', 'transFormatID' : 'INT', 'aspectRatioID' : 'INT', 
							'primaryAudioID' : 'INT', 'discCountID' : 'INT', 'regionCodeID' : 'INT', 'oflcRatingID' : 'INT', 
							'runTimeID' : 'INT', 'genresID' : 'INT', 'actorsID' : 'INT', 'distributorID' : 'INT', 
							'releaseDate' : 'VARCHAR(24)', 'got' : 'INT', 'catalogNoID' : 'INT', 'formatID' : 'INT', 
							'downloaded' : 'INT'
						}
				}
			},
		# Table foreign keys, their table nemes, column names and their values	
		# 'c' prefix indicates that it is a constrained (FK) table to a main table
		'fk' :
			{
			'c_productType' :
				{
					'id' :
					{
						'productTypeID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY'
					},
					'columns' : 
					{
						'productType' : 'VARCHAR(16)'
					}
				},
			'c_imageFolder' : 
				{
					'id' :
					{
						'imageFolderID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY'
					},
					'columns' : 
					{
						'imageFolder' : 'VARCHAR(128)'
					}
				},
			'c_vidFormat' : 
				{ 
					'id' :
					{
						'vidFormatID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY'
					},
					'columns' : 
					{
						'vidformat' : 'VARCHAR(16)'
					}
				},
			'c_transFormat' : 
				{
					'id' :
					{
						'transFormatID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY'
					},
					'columns' : 
					{
						'transFormat' : 'VARCHAR(16)'
					}
				},
			'c_aspectRatio' : 
				{
					'id' :
					{
						'aspectRatioID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY'
					},
					'columns' : 
					{
						'aspectRatio' : 'VARCHAR(16)'
					}
				},
			'c_primaryAudio' : 
				{
					'id' :
					{
						'primaryAudioID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY'
					},
					'columns' : 
					{
						'primaryAudio' : 'VARCHAR(16)'
					}
				},
			'c_discCount' : 
				{
					'id' :
					{
						'discCountID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY'
					},
					'columns' : 
					{
						'discCount' : 'INT'
					}
				},
			'c_regionCode' : 
				{
					'id' :
					{
						'regionCodeID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY'
					},
					'columns' : 
					{
						'regionCode' : 'VARCHAR(8)'
					}
				},
			'c_oflcRating' : 
				{
					'id' :
					{
						'oflcRatingID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY'
					},
					'columns' : 
					{
						'oflcRating' : 'VARCHAR(8)'
					}
				},
			'c_runTime' : 
				{
					'id' :
					{
						'runTimeID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY'
					},
					'columns' : 
					{
						'runTime' : 'VARCHAR(12)'
					}
				},
			'c_genres' : 
				{
					'id' :
					{
						'genresID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY'
					},
					'columns' : 
					{
						'genres' : 'VARCHAR(4)'
					}
				},
			'c_actors' : 
				{
					'id' :
					{
						'actorsID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY'
					},
					'columns' : 
					{
						'actors' : 'VARCHAR(256)'
					}	
				},
			'c_distributor' : 
				{
					'id' :
					{
						'distributorID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY'
					},
					'columns' : 
					{
						'distributor' : 'VARCHAR(64)'
					}		
				},
			'c_catalogNo' : 
				{
					'id' :
					{
						'catalogNoID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY'
					},
					'columns' : 
					{
						'catalogNo' : 'INT'
					}
				},
			'c_format' : 
				{
					'id' :
					{
						'formatID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY'
					},
					'columns' : 
					{
						'format' : 'VARCHAR(16)'
					} 
				},
			'c_retailer' : 
				{
					'id' :
					{
						'retailerID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY'
					},
					'columns' : 
					{
						'retailer' : 'VARCHAR(64)'
					} 
				}
			}
		}