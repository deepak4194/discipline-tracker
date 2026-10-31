-- Run this once in Supabase SQL Editor.
-- This allows the Streamlit app's publishable/anon key to read and update tracker rows.
-- Keep your Streamlit app URL private if you don't want others changing your tracker.

CREATE POLICY "Allow tracker reads"
ON public.daily_progress
FOR SELECT
TO anon
USING (true);

CREATE POLICY "Allow tracker inserts"
ON public.daily_progress
FOR INSERT
TO anon
WITH CHECK (true);

CREATE POLICY "Allow tracker updates"
ON public.daily_progress
FOR UPDATE
TO anon
USING (true)
WITH CHECK (true);
