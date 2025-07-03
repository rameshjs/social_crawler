# Social Crawler

A FastAPI-based social media crawler that fetches and stores data from Reddit, Hacker News, and YouTube. The application uses scheduled jobs to continuously collect trending posts, comments, and videos from multiple platforms.

## Features

### 🔴 Reddit Integration
- Fetches latest posts from specified subreddits
- Stores post data and comments in MongoDB
- Uses PRAW (Python Reddit API Wrapper)
- Scheduled crawling every 5 minutes

### 🟠 Hacker News Integration
- Two-service architecture: fetch latest post IDs and process individual posts
- Uses Redis queue for post ID management
- Fetches from Hacker News Firebase API
- Stores structured post data in MongoDB
- Scheduled: fetch every 60 seconds, process every 30 seconds

### 📺 YouTube Integration
- Fetches globally trending videos
- Collects latest comments from popular videos
- Uses YouTube Data API v3
- Two independent services: trending videos and comments
- Scheduled every 5 minutes

## Architecture

```
social_crawler/
├── reddit_crawler/           # Reddit crawling service
├── hackernews_crawler/       # Hacker News crawling service
├── youtube_crawler/          # YouTube crawling service
├── scheduler.py              # APScheduler configuration
├── config.py                 # Configuration management
├── main.py                   # FastAPI application
├── docker-compose.yml        # Docker orchestration
└── requirements.txt          # Python dependencies
```

## Prerequisites

- Python 3.10+
- Docker and Docker Compose
- Redis server
- MongoDB server
- API keys for Reddit and YouTube

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd social_crawler
   ```

2. **Set up environment variables**
   ```bash
   cp env.sample .env
   # Edit .env with your API keys and configuration
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start services with Docker**
   ```bash
   docker-compose up --build
   ```

## Configuration

### Environment Variables

```bash
# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/
MONGO_DB_NAME=reddit_crawler
MONGO_COLLECTION_NAME=posts

# Reddit API Configuration
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=fastapi-reddit-crawler
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
REDDIT_CRAWL_INTERVAL_SECONDS=300

# Hacker News Configuration
HACKERNEWS_FETCH_INTERVAL_SECONDS=60

# YouTube Configuration
YOUTUBE_API_KEY=your_youtube_api_key
YOUTUBE_FETCH_INTERVAL_SECONDS=300
```

## API Keys Setup

### Reddit API
1. Go to https://www.reddit.com/prefs/apps
2. Create a new application
3. Set type to "script"
4. Copy client ID and secret

### YouTube API
1. Go to Google Cloud Console
2. Enable YouTube Data API v3
3. Create credentials (API key)
4. Set quota limits appropriately

## Usage

### Running the Application

**Development:**
```bash
python -m uvicorn main:app --reload
```

**Production with Docker:**
```bash
docker-compose up --build
```

## Data Storage

### MongoDB Collections

- `posts` - Reddit posts and comments
- `hackernews_posts` - Hacker News stories
- `youtube_trending_videos` - YouTube trending videos
- `youtube_latest_comments` - YouTube comments

### Redis Keys

- `hackernews:post_queue` - Hacker News post ID queue
- `hackernews:last_fetched` - Last fetched Hacker News post ID
- `apscheduler.jobs` - Scheduler job storage
- `apscheduler.run_times` - Scheduler run times


### Adding New Services

1. Create a new crawler package following the existing pattern
2. Implement service modules with fetch and save functions
3. Add job definitions in the crawler module
4. Update `main.py` to register the new jobs
5. Add configuration variables to `config.py`
6. Update environment variables in `env.sample`

## Monitoring

### Logs
The application logs all crawling activities, including:
- API requests and responses
- Database operations
- Job execution status
- Error messages

### Health Checks
Monitor the application health through:
- Docker container status
- MongoDB connection
- Redis connection
- API response times

## Troubleshooting

### Common Issues

**Redis Connection Errors:**
- Ensure Redis server is running
- Check Redis host and port configuration
- Clear Redis keys if job references are corrupted

**MongoDB Connection Errors:**
- Verify MongoDB server is running
- Check connection string in environment variables
- Ensure database permissions are correct

**API Rate Limits:**
- Monitor API quota usage
- Implement exponential backoff for retries
- Consider reducing crawl frequency

**Module Import Errors:**
- Clear Redis scheduler keys if module names have changed
- Restart the application after configuration changes

## Contributing

1. Follow the existing code patterns and structure
2. Add proper error handling and logging
3. Include tests for new features
4. Update documentation for any changes
5. Follow the cursor rules and Python best practices

