CREATE DATABASE mywebsearch_2022_05_07; 
CREATE USER search_user WITH PASSWORD 'Search@143';
ALTER ROLE search_user SET client_encoding TO 'utf8'; 
ALTER ROLE search_user SET default_transaction_isolation TO 'read committed'; 
ALTER ROLE search_user SET timezone TO 'UTC'; 
GRANT ALL PRIVILEGES ON DATABASE mywebsearch_2022_05_07 TO search_user;
GRANT USAGE ON SCHEMA public TO search_user;
GRANT CREATE ON SCHEMA public TO search_user;
ALTER DATABASE mywebsearch_2022_05_07 OWNER TO search_user;