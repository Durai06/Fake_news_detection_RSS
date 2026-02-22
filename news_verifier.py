import re
import requests
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsVerifier:
    def __init__(self):
        # RSS Feeds from trusted Indian news sources
        self.rss_feeds = {
            'The Hindu': 'https://www.thehindu.com/news/feeder/default.rss',
            'Indian Express': 'https://indianexpress.com/feed/',
            'Times of India': 'https://timesofindia.indiatimes.com/rssfeedstopstories.cms',
            'NDTV': 'https://feeds.feedburner.com/ndtvnews-top-stories'
        }
        
        # Common stop words to ignore in keyword extraction
        self.stop_words = {
            'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'is', 'are', 'was', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'shall', 'should', 'may', 'might', 'must', 'can', 'could',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'them', 'their', 'this',
            'that', 'these', 'those', 'who', 'whom', 'which', 'what', 'say', 'said',
            'told', 'according', 'report', 'reports', 'reported', 'news', 'india',
            'new', 'old', 'first', 'last', 'next', 'previous', 'one', 'two', 'three',
            'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'many', 'much',
            'few', 'several', 'all', 'some', 'any', 'every', 'each', 'both', 'neither',
            'either', 'none', 'no', 'not', 'only', 'just', 'very', 'too', 'so',
            'such', 'same', 'different', 'other', 'another', 'more', 'most', 'less',
            'least', 'better', 'best', 'worse', 'worst', 'now', 'then', 'today',
            'tomorrow', 'yesterday', 'here', 'there', 'everywhere', 'anywhere',
            'nowhere', 'always', 'never', 'sometimes', 'often', 'usually',
            'frequently', 'rarely', 'seldom', 'already', 'yet', 'still',
            'almost', 'nearly', 'hardly', 'merely', 'simply'
        }
        
        # Common patterns for news headlines
        self.patterns = {
            'govt': r'\b(government|govt|centre|ministry|minister|pm|modi|parliament|mp|mla|election|voter|party|bjp|congress|aap|tmc|nda|upa)\b',
            'finance': r'\b(rbi|banking|bank|finance|economy|gdp|inflation|rupee|tax|budget|stocks|market|sensex|nifty|investment|loan|credit|debit|interest|fd|rd|mutual fund|insurance)\b',
            'tech': r'\b(tech|technology|digital|ai|artificial intelligence|cyber|internet|upi|app|smartphone|mobile|android|ios|windows|software|hardware|computer|laptop|tablet|gadget|innovation)\b',
            'sports': r'\b(cricket|ipl|world cup|sport|match|tournament|team|player|cricketer|batsman|bowler|wicket|run|goal|fifa|olympics|athlete|tennis|football|hockey|badminton|kabaddi)\b',
            'international': r'\b(us|usa|america|china|russia|uk|britain|pakistan|border|international|global|world|foreign|diplomat|embassy|un|united nations|wto|imf|world bank|bilateral|multilateral)\b',
            'health': r'\b(health|hospital|doctor|patient|disease|virus|covid|corona|vaccine|medicine|treatment|surgery|medical|healthcare|fitness|wellness|nutrition|diet|exercise|yoga|ayush)\b',
            'education': r'\b(education|school|college|university|student|teacher|professor|exam|result|admission|scholarship|degree|diploma|course|curriculum|board|cbse|icse|ncert|upsc)\b',
            'crime': r'\b(crime|criminal|police|thief|robbery|murder|attack|assault|theft|fraud|scam|corruption|arrest|jail|prison|court|judge|lawyer|legal|case|verdict|sentence)\b',
            'environment': r'\b(environment|climate|weather|rain|storm|flood|earthquake|disaster|pollution|green|eco|sustainable|renewable|forest|wildlife|animal|plant|tree|water|air)\b',
            'entertainment': r'\b(entertainment|movie|film|cinema|actor|actress|director|producer|singer|song|music|dance|theatre|drama|serial|tv|television|web series|ott|netflix|amazon prime|hotstar)\b'
        }

    def fetch_rss_feed(self, url):
        """
        Fetch and parse RSS feed using requests and xml.etree
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse XML
            root = ET.fromstring(response.content)
            
            # Find all items (RSS 2.0) or entries (Atom)
            items = []
            
            # Try RSS 2.0 format
            for item in root.findall('.//item'):
                title = item.find('title')
                link = item.find('link')
                pubDate = item.find('pubDate')
                description = item.find('description')
                
                if title is not None and title.text:
                    items.append({
                        'title': title.text.strip(),
                        'link': link.text.strip() if link is not None and link.text else '#',
                        'published': pubDate.text.strip() if pubDate is not None and pubDate.text else datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'summary': description.text.strip()[:200] + '...' if description is not None and description.text else ''
                    })
            
            # Try Atom format if no RSS items found
            if not items:
                for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
                    title = entry.find('{http://www.w3.org/2005/Atom}title')
                    link = entry.find('{http://www.w3.org/2005/Atom}link')
                    published = entry.find('{http://www.w3.org/2005/Atom}published')
                    summary = entry.find('{http://www.w3.org/2005/Atom}summary')
                    
                    if title is not None and title.text:
                        link_href = link.get('href') if link is not None else '#'
                        items.append({
                            'title': title.text.strip(),
                            'link': link_href,
                            'published': published.text.strip() if published is not None and published.text else datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'summary': summary.text.strip()[:200] + '...' if summary is not None and summary.text else ''
                        })
            
            logger.info(f"Fetched {len(items)} items from {url}")
            return items
            
        except requests.RequestException as e:
            logger.error(f"Request error for {url}: {str(e)}")
            return []
        except ET.ParseError as e:
            logger.error(f"XML parse error for {url}: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {str(e)}")
            return []

    def extract_keywords(self, text):
        """
        Extract keywords from user input using rule-based processing
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\-]', ' ', text)
        
        # Split into words
        words = text.split()
        
        # Remove stop words and short words
        keywords = [word for word in words if word not in self.stop_words and len(word) > 2]
        
        # Extract important named entities (words starting with capital letters in original text)
        # But since we lowercased, we need to check original case
        original_words = text.split()  # This is still lowercase, so we'll use a different approach
        
        # Extract phrases (2-3 word combinations) that might be important
        phrases = []
        for i in range(len(words) - 1):
            if i < len(words) - 1:
                # Two-word phrases
                if words[i] not in self.stop_words and words[i+1] not in self.stop_words:
                    phrase = f"{words[i]} {words[i+1]}"
                    phrases.append(phrase)
            
            if i < len(words) - 2:
                # Three-word phrases
                if (words[i] not in self.stop_words and 
                    words[i+1] not in self.stop_words and 
                    words[i+2] not in self.stop_words):
                    phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
                    phrases.append(phrase)
        
        # Count word frequency
        word_freq = Counter(keywords)
        
        # Get top keywords based on frequency
        top_keywords = []
        for word, freq in word_freq.most_common(15):
            top_keywords.append(word)
        
        # Add important phrases (avoiding duplicates)
        for phrase in phrases[:10]:
            # Check if phrase is not already represented by individual words
            phrase_words = phrase.split()
            if not all(word in top_keywords for word in phrase_words):
                # Check if phrase is significantly different from existing keywords
                is_duplicate = False
                for kw in top_keywords:
                    if phrase in kw or kw in phrase:
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    top_keywords.append(phrase)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_keywords = []
        for kw in top_keywords:
            if kw not in seen:
                seen.add(kw)
                unique_keywords.append(kw)
        
        logger.info(f"Extracted keywords: {unique_keywords[:15]}")
        return unique_keywords[:15]  # Return top 15 keywords

    def fetch_all_news(self):
        """
        Fetch news from all RSS feeds
        """
        all_articles = []
        
        for source, feed_url in self.rss_feeds.items():
            logger.info(f"Fetching news from {source}...")
            articles = self.fetch_rss_feed(feed_url)
            
            # Add source information to each article
            for article in articles:
                article['source'] = source
            
            all_articles.extend(articles)
        
        # Remove duplicates based on title (some stories might appear in multiple feeds)
        seen_titles = set()
        unique_articles = []
        
        for article in all_articles:
            title_lower = article['title'].lower()
            if title_lower not in seen_titles:
                seen_titles.add(title_lower)
                unique_articles.append(article)
        
        logger.info(f"Total unique articles fetched: {len(unique_articles)}")
        return unique_articles

    def calculate_similarity(self, user_keywords, headline):
        """
        Calculate similarity between user keywords and headline using advanced rule-based matching
        """
        # Convert headline to lowercase
        headline_lower = headline.lower()
        
        # Calculate matches with different weights
        exact_matches = 0
        partial_matches = 0
        phrase_matches = 0
        
        for keyword in user_keywords:
            keyword_lower = keyword.lower()
            
            # Check for exact phrase match (highest weight)
            if keyword_lower in headline_lower:
                if len(keyword.split()) > 1:  # Multi-word phrase
                    phrase_matches += 2
                else:
                    exact_matches += 1
            else:
                # Check for partial matches (word-level)
                keyword_words = keyword_lower.split()
                matched_words = 0
                
                for word in keyword_words:
                    if len(word) > 3 and word in headline_lower:
                        matched_words += 1
                
                if matched_words > 0:
                    partial_matches += matched_words / len(keyword_words)
        
        # Calculate similarity score
        total_keywords = len(user_keywords)
        if total_keywords == 0:
            return 0
        
        base_score = (exact_matches + partial_matches + phrase_matches) / total_keywords
        
        # Apply pattern matching bonus
        pattern_bonus = 0
        for pattern_name, pattern in self.patterns.items():
            headline_matches = re.findall(pattern, headline_lower)
            if headline_matches:
                for keyword in user_keywords:
                    if re.search(pattern, keyword.lower()):
                        pattern_bonus += 0.1 * len(headline_matches)
                        break
        
        # Apply length penalty for very short headlines
        length_penalty = 0
        if len(headline_lower.split()) < 3:
            length_penalty = 0.2
        elif len(headline_lower.split()) < 5:
            length_penalty = 0.1
        
        final_score = min(base_score + pattern_bonus - length_penalty, 1.0)
        
        return max(final_score, 0)  # Ensure non-negative

    def verify_news(self, user_input):
        """
        Main verification function
        """
        # Step 1: Extract keywords from user input
        keywords = self.extract_keywords(user_input)
        
        # Step 2: Fetch latest news from all sources
        articles = self.fetch_all_news()
        
        # Step 3: Compare with headlines
        matches = []
        for article in articles:
            similarity = self.calculate_similarity(keywords, article['title'])
            if similarity > 0.25:  # Lower threshold to catch more potential matches
                matches.append({
                    'title': article['title'],
                    'link': article['link'],
                    'source': article['source'],
                    'similarity': round(similarity, 2),
                    'published': article.get('published', 'Recently')
                })
        
        # Step 4: Sort matches by similarity
        matches.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Step 5: Determine verification status with refined logic
        if len(matches) >= 3:
            # Check top matches
            top_matches = matches[:5]
            avg_similarity = sum(m['similarity'] for m in top_matches) / len(top_matches)
            
            if avg_similarity > 0.6:
                status = "Likely Real ✅"
                confidence = "High confidence"
            elif avg_similarity > 0.4:
                status = "Partially Verified ⚠️"
                confidence = "Medium confidence"
            else:
                status = "Possibly Fake / Unverified ❌"
                confidence = "Low confidence"
        elif len(matches) == 2:
            if matches[0]['similarity'] > 0.7 or (matches[0]['similarity'] > 0.5 and matches[1]['similarity'] > 0.4):
                status = "Partially Verified ⚠️"
                confidence = "Limited sources"
            else:
                status = "Possibly Fake / Unverified ❌"
                confidence = "Insufficient evidence"
        elif len(matches) == 1:
            if matches[0]['similarity'] > 0.8:
                status = "Partially Verified ⚠️"
                confidence = "Single source"
            else:
                status = "Possibly Fake / Unverified ❌"
                confidence = "Single low-quality match"
        else:
            status = "Possibly Fake / Unverified ❌"
            confidence = "No matching sources"
        
        # Prepare result
        result = {
            'status': status,
            'confidence': confidence,
            'matching_sources': len(set(m['source'] for m in matches)),
            'total_matches': len(matches),
            'keywords_used': keywords[:10],  # Show top 10 keywords
            'related_news': matches[:10]  # Top 10 matches
        }
        
        logger.info(f"Verification complete: {status} with {len(matches)} matches")
        return result