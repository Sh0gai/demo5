-- Migration: Add archived column to pizza and customer tables
-- Run this if you already have an existing database to add the archived functionality

-- Add archived column to customer table
ALTER TABLE customer ADD COLUMN archived BOOLEAN DEFAULT FALSE;

-- Add archived column to pizza table
ALTER TABLE pizza ADD COLUMN archived BOOLEAN DEFAULT FALSE;

-- Update existing records to not be archived
UPDATE customer SET archived = FALSE WHERE archived IS NULL;
UPDATE pizza SET archived = FALSE WHERE archived IS NULL;
