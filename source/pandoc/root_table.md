--------------------------------------------------------------------------
Table Type 			Table Name 			       Table ID
-----------------   ----------------------  -----------------------------
User Table 			User Table Name 		 User Table ID

User Meta Table 	__User Table ID.META 	 User Table ID – 1

User Root Table 	__User Table ID.ROOT 	 User Table ID – 2

First Root Table 	__first_root_table 		 111
--------------------------------------------------------------------------
: 表1 内部表表名和ID对应关系



--------------------------------------------------------------------------
Table Type  		             Table Rowkey
------------------  ------------------------------------------------------
User Table 			   User Table Rowkey Columns

User Meta Table 	   Cluster ID + Userr Table ID + User Table Rowkey Columns

User Root Table 	   Cluster ID + User Meta Table ID + User Table ID + 
                           User Table Rowkey Columns

First Root Table 	   Cluster ID + User Root Table ID
--------------------------------------------------------------------------
: 表2 Rowkey构成规则
