-- This file runs automatically when PostgreSQL container starts
-- It enables the extensions we need

-- PostGIS: adds GPS/location support to PostgreSQL
-- Allows us to store coordinates and run geo queries like
-- "find all laws that apply within this boundary"
CREATE EXTENSION IF NOT EXISTS postgis;

-- pgvector: adds AI vector support to PostgreSQL
-- Allows us to store law embeddings and run similarity searches
-- "find laws most similar to this question"
CREATE EXTENSION IF NOT EXISTS vector;

-- pg_trgm: adds fuzzy text search support
-- Allows us to search laws by keyword even with typos
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Confirm extensions are installed
SELECT name, default_version 
FROM pg_available_extensions 
WHERE name IN ('postgis', 'vector', 'pg_trgm');