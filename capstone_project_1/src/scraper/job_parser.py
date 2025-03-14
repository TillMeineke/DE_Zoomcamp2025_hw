"""
Job Parser for Stepstone.

This module provides functionality to parse and extract structured data
from Stepstone job listings.
"""

import re
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

from bs4 import BeautifulSoup, Tag


class JobParser:
    """
    A class to parse job listings from Stepstone.de.
    
    This parser extracts structured data from job listing HTML elements.
    It provides methods for parsing both job cards (search results) and
    detailed job pages.
    """
    
    def parse_job_card(self, job_element: Tag) -> Optional[Dict[str, Any]]:
        """
        Parse a job card element from the search results page.
        
        Args:
            job_element: BeautifulSoup Tag object representing a job card
            
        Returns:
            Dictionary containing extracted job data or None if parsing fails
        """
        try:
            # Extract job title and URL
            job_title = job_element.get_text(strip=True)
            job_url = job_element.get("href", "")
            
            # Create job listing dictionary with basic information
            job_data = {
                "job_id": self._extract_job_id(job_url),
                "job_title": job_title,
                "job_url": job_url,
                "scrape_date": datetime.now().isoformat(),
            }
            
            # Find the parent article that contains additional information
            parent_article = self._find_parent_article(job_element)
            if parent_article:
                # Extract additional data from the parent article
                company_name = self._extract_company_name(parent_article)
                location = self._extract_location(parent_article)
                posting_date = self._extract_posting_date(parent_article)
                
                # Add additional information to the job data
                if company_name:
                    job_data["company_name"] = company_name
                if location:
                    job_data["location"] = location
                if posting_date:
                    job_data["posting_date"] = posting_date
            
            return job_data
            
        except Exception as e:
            print(f"Error parsing job card: {str(e)}")
            return None
            
    def parse_job_details(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Parse the detailed job page to extract comprehensive information.
        
        Args:
            soup: BeautifulSoup object of the job detail page
            
        Returns:
            Dictionary containing detailed job information
        """
        job_details = {}
        
        try:
            # Extract job title
            title_element = soup.find("h1")
            if title_element:
                job_details["job_title"] = title_element.get_text(strip=True)
            
            # Extract company name
            company_element = soup.find("span", {"data-at": "job-header-company"})
            if company_element:
                job_details["company_name"] = company_element.get_text(strip=True)
            
            # Extract job description
            description_element = soup.find("div", {"data-at": "job-description"})
            if description_element:
                job_details["description"] = description_element.get_text(strip=True)
                
                # Extract skills from the description
                job_details["skills"] = self._extract_skills(description_element.get_text())
            
            # Extract salary information if available
            salary_element = soup.find("span", {"data-at": "job-header-salary"})
            if salary_element:
                job_details["salary"] = self._parse_salary(salary_element.get_text(strip=True))
            
            # Extract employment type
            employment_type_element = soup.find("span", {"data-at": "job-header-employment-type"})
            if employment_type_element:
                job_details["employment_type"] = employment_type_element.get_text(strip=True)
            
        except Exception as e:
            print(f"Error parsing job details: {str(e)}")
        
        return job_details
    
    def _extract_job_id(self, job_url: str) -> str:
        """
        Extract the job ID from the URL.
        
        Args:
            job_url: URL of the job posting
            
        Returns:
            Job ID as a string
        """
        try:
            # Extract job ID from URL pattern
            match = re.search(r"--(\d+)-", job_url)
            if match:
                return match.group(1)
            else:
                return job_url.split("/")[-1].split(".")[0]
        except Exception:
            return f"unknown-{datetime.now().timestamp()}"
    
    def _find_parent_article(self, element: Tag) -> Optional[Tag]:
        """
        Find the parent article element containing additional job information.
        
        Args:
            element: BeautifulSoup Tag object
            
        Returns:
            Parent article Tag if found, None otherwise
        """
        parent = element
        max_levels = 5  # Limit search to 5 levels up to avoid infinite loops
        
        for _ in range(max_levels):
            if parent is None:
                return None
            
            if parent.name == "article":
                return parent
            
            parent = parent.parent
            
        return None
    
    def _extract_company_name(self, article: Tag) -> Optional[str]:
        """
        Extract the company name from the article element.
        
        Args:
            article: Article Tag object
            
        Returns:
            Company name as a string if found, None otherwise
        """
        company_element = article.find(attrs={"data-at": "job-item-company-name"})
        if company_element:
            return company_element.get_text(strip=True)
        return None
    
    def _extract_location(self, article: Tag) -> Optional[str]:
        """
        Extract the job location from the article element.
        
        Args:
            article: Article Tag object
            
        Returns:
            Location as a string if found, None otherwise
        """
        location_element = article.find(attrs={"data-at": "job-item-location"})
        if location_element:
            return location_element.get_text(strip=True)
        return None
    
    def _extract_posting_date(self, article: Tag) -> Optional[str]:
        """
        Extract the posting date from the article element.
        
        Args:
            article: Article Tag object
            
        Returns:
            Posting date as a string if found, None otherwise
        """
        date_element = article.find("span", {"data-at": "job-item-timeago"})
        if date_element and date_element.find("time"):
            return date_element.find("time").get_text(strip=True)
        return None
    
    def _extract_skills(self, description: str) -> List[str]:
        """
        Extract mentioned skills from job description.
        
        This is a simple implementation that looks for common data science and
        technology skills in the description text.
        
        Args:
            description: Job description text
            
        Returns:
            List of identified skills
        """
        skills = []
        
        # Common data science and tech skills to look for
        skill_patterns = [
            r"python", r"sql", r"r\s+language", r"\br\b", r"java", r"javascript", 
            r"typescript", r"react", r"vue", r"angular", r"docker", r"kubernetes",
            r"aws", r"azure", r"gcp", r"cloud", r"hadoop", r"spark", r"kafka",
            r"pandas", r"numpy", r"scikit.learn", r"tensorflow", r"pytorch", 
            r"machine\s+learning", r"deep\s+learning", r"nlp", r"natural\s+language\s+processing",
            r"computer\s+vision", r"data\s+visualization", r"tableau", r"power\s+bi",
            r"excel", r"statistics", r"mathematics", r"algorithms", r"git", 
            r"jenkins", r"ci/cd", r"agile", r"scrum"
        ]
        
        # Convert description to lowercase for case-insensitive matching
        description_lower = description.lower()
        
        # Find matching skills in the description
        for pattern in skill_patterns:
            if re.search(pattern, description_lower):
                # Convert skill to a standardized format
                skill = pattern.replace(r"\s+", " ")
                skill = skill.replace(r"\b", "")
                
                # Add the skill to our list
                skills.append(skill)
        
        return skills
    
    def _parse_salary(self, salary_text: str) -> Dict[str, Any]:
        """
        Parse salary information into a structured format.
        
        Args:
            salary_text: Text containing salary information
            
        Returns:
            Dictionary containing structured salary data
        """
        salary_data = {"raw": salary_text}
        
        try:
            # Extract salary range if present
            range_match = re.search(r"(\d+[\.,]\d+)\s*-\s*(\d+[\.,]\d+)", salary_text)
            if range_match:
                min_salary = float(range_match.group(1).replace(".", "").replace(",", "."))
                max_salary = float(range_match.group(2).replace(".", "").replace(",", "."))
                
                salary_data["min_salary"] = min_salary
                salary_data["max_salary"] = max_salary
                salary_data["avg_salary"] = (min_salary + max_salary) / 2
            
            # Extract currency
            currency_match = re.search(r"(€|\$|£|EUR|USD|GBP)", salary_text)
            if currency_match:
                salary_data["currency"] = currency_match.group(1)
            
            # Extract frequency (yearly, monthly, etc.)
            if re.search(r"year|yearly|annual|p\.a\.|per\s+annum", salary_text, re.IGNORECASE):
                salary_data["frequency"] = "yearly"
            elif re.search(r"month|monthly", salary_text, re.IGNORECASE):
                salary_data["frequency"] = "monthly"
            elif re.search(r"hour|hourly", salary_text, re.IGNORECASE):
                salary_data["frequency"] = "hourly"
            elif re.search(r"day|daily", salary_text, re.IGNORECASE):
                salary_data["frequency"] = "daily"
            else:
                salary_data["frequency"] = "unknown"
                
        except Exception:
            # If parsing fails, just keep the raw text
            pass
            
        return salary_data