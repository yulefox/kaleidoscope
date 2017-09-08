# collation

国际化的过程中, 字符集的不同导致 MySQL 存储过程中字符串的比较错误:

    ERROR 1267 (HY000): Illegal mix of collations (utf8_general_ci,IMPLICIT) and (utf8_unicode_ci,IMPLICIT) for operation '>='

    ERROR 1253 (42000): COLLATION 'utf8_unicode_ci' is not valid for CHARACTER SET 'latin1' 

