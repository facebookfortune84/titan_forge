"""Blog management endpoints for content marketing and SEO."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import db_models, schemas
from app.database import get_db
from app.dependencies import get_current_active_user

router = APIRouter(prefix="/blog", tags=["blog"])


@router.get("", response_model=List[schemas.BlogPostResponse])
async def list_blog_posts(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    published_only: bool = Query(True),
):
    """List blog posts with pagination. By default, shows only published posts."""
    query = db.query(db_models.BlogPost)
    
    if published_only:
        query = query.filter(db_models.BlogPost.published == True)
    
    posts = query.order_by(db_models.BlogPost.created_at.desc()).offset(skip).limit(limit).all()
    return posts


@router.get("/slug/{slug}", response_model=schemas.BlogPostDetailResponse)
async def get_post_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get a single blog post by slug."""
    post = db.query(db_models.BlogPost).filter(
        db_models.BlogPost.slug == slug,
        db_models.BlogPost.published == True
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    return post


@router.get("/{post_id}", response_model=schemas.BlogPostDetailResponse)
async def get_post(post_id: UUID, db: Session = Depends(get_db)):
    """Get a single blog post by ID."""
    post = db.query(db_models.BlogPost).filter(
        db_models.BlogPost.id == post_id,
        db_models.BlogPost.published == True
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    return post


@router.post("", response_model=schemas.BlogPostResponse, status_code=201)
async def create_blog_post(
    post_data: schemas.BlogPostCreate,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_active_user),
):
    """Create a new blog post. Only for authenticated users."""
    # Check if slug already exists
    existing = db.query(db_models.BlogPost).filter(
        db_models.BlogPost.slug == post_data.slug
    ).first()
    
    if existing:
        raise HTTPException(status_code=409, detail="Blog post with this slug already exists")
    
    db_post = db_models.BlogPost(
        title=post_data.title,
        slug=post_data.slug,
        content=post_data.content,
        excerpt=post_data.excerpt,
        featured_image_url=post_data.featured_image_url,
        tags=post_data.tags or [],
        meta_title=post_data.meta_title or post_data.title,
        meta_description=post_data.meta_description or post_data.excerpt,
        author_id=current_user.id,
        published=post_data.published,
        published_at=datetime.utcnow() if post_data.published else None,
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    return db_post


@router.put("/{post_id}", response_model=schemas.BlogPostResponse)
async def update_blog_post(
    post_id: UUID,
    post_data: schemas.BlogPostUpdate,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_active_user),
):
    """Update a blog post. Only the author or superuser can update."""
    post = db.query(db_models.BlogPost).filter(db_models.BlogPost.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    if post.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    
    # Check slug uniqueness if changing slug
    if post_data.slug and post_data.slug != post.slug:
        existing = db.query(db_models.BlogPost).filter(
            db_models.BlogPost.slug == post_data.slug
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail="Blog post with this slug already exists")
    
    # Update fields
    update_data = post_data.dict(exclude_unset=True)
    
    # Handle published status change
    if "published" in update_data:
        if update_data["published"] and not post.published_at:
            post.published_at = datetime.utcnow()
        post.published = update_data["published"]
    
    for field, value in update_data.items():
        if field != "published":
            setattr(post, field, value)
    
    db.commit()
    db.refresh(post)
    
    return post


@router.delete("/{post_id}", status_code=204)
async def delete_blog_post(
    post_id: UUID,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_active_user),
):
    """Delete a blog post. Only the author or superuser can delete."""
    post = db.query(db_models.BlogPost).filter(db_models.BlogPost.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    if post.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    db.delete(post)
    db.commit()
    
    return None


@router.get("/tags/list", response_model=List[str])
async def list_tags(db: Session = Depends(get_db)):
    """Get all unique tags used across published posts."""
    posts = db.query(db_models.BlogPost).filter(
        db_models.BlogPost.published == True
    ).all()
    
    tags_set = set()
    for post in posts:
        if post.tags:
            tags_set.update(post.tags)
    
    return sorted(list(tags_set))


@router.get("/tags/{tag}", response_model=List[schemas.BlogPostResponse])
async def get_posts_by_tag(
    tag: str,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    """Get all blog posts with a specific tag."""
    posts = db.query(db_models.BlogPost).filter(
        db_models.BlogPost.published == True,
        db_models.BlogPost.tags.contains([tag])
    ).order_by(db_models.BlogPost.created_at.desc()).offset(skip).limit(limit).all()
    
    return posts


# Blog auto-publishing configuration
BLOG_TOPICS = [
    "AI Automation Trends in 2026",
    "Cost Reduction Through Intelligent Automation",
    "Enterprise AI Implementation Best Practices",
    "Digital Transformation ROI Analysis",
    "Workflow Optimization with AI Agents",
    "Machine Learning in Business Operations",
    "Future of Autonomous Systems",
    "Cloud-Native AI Architecture",
    "Data Privacy in AI Solutions",
    "Real-Time Decision Making with AI",
]


class AutoPublishRequest(BaseModel):
    """Request to trigger auto-publish of blog post."""
    topic: Optional[str] = None


@router.post("/auto-publish")
async def auto_publish_blog(
    request: AutoPublishRequest = None,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_active_user),
):
    """
    Automatically generate and publish a blog post via marketing agent.
    Agent selects topic and generates content based on predefined list.
    """
    import random
    import re
    from datetime import datetime as dt
    
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Only admins can trigger auto-publish")
    
    # Select topic
    topic = request.topic if request and request.topic else random.choice(BLOG_TOPICS)
    
    # Generate slug from topic
    slug = re.sub(r'[^a-z0-9]+', '-', topic.lower()).strip('-')
    
    # Check if post with this slug already exists today
    today = dt.utcnow().date()
    existing = db.query(db_models.BlogPost).filter(
        db_models.BlogPost.slug == slug
    ).first()
    
    if existing:
        # If it exists, add date suffix
        slug = f"{slug}-{today.isoformat()}"
    
    # Generate content (in production, this would call the marketing agent)
    content = f"""# {topic}

## Introduction
This article explores {topic.lower()} and its impact on modern business operations.

## Key Points
- **Efficiency Gains**: Automated systems deliver measurable ROI within 90 days
- **Cost Reduction**: Typical implementations reduce operational costs by 30-50%
- **Scalability**: AI-powered solutions scale with minimal additional overhead
- **Compliance**: Built-in governance ensures regulatory adherence

## Implementation Strategy
Organizations should follow a phased approach:
1. Assessment of current workflows
2. Identification of automation opportunities  
3. Pilot implementation with key processes
4. Scale to enterprise level

## Conclusion
{topic} represents a critical opportunity for forward-thinking organizations to improve efficiency and reduce costs. Early adoption provides competitive advantages in the market.

---
*This article was automatically generated on {dt.utcnow().strftime('%B %d, %Y')} at 9:00 AM UTC*
"""

    # Create blog post
    blog_post = db_models.BlogPost(
        title=topic,
        slug=slug,
        content=content,
        excerpt=f"Discover insights on {topic} and how to leverage it for business growth.",
        tags=["automation", "ai", "business", "implementation"],
        meta_title=f"{topic} - TitanForge Blog",
        meta_description=f"Learn about {topic} and best practices for implementation.",
        author_id=current_user.id,
        published=True,
        published_at=dt.utcnow(),
    )
    
    db.add(blog_post)
    db.commit()
    db.refresh(blog_post)
    
    return {
        "status": "published",
        "message": f"Blog post '{topic}' published successfully",
        "post_id": str(blog_post.id),
        "slug": blog_post.slug,
        "title": blog_post.title,
        "url": f"/blog/{blog_post.slug}",
    }
