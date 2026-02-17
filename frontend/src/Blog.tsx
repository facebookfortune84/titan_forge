import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface BlogPost {
  id: string;
  title: string;
  slug: string;
  excerpt: string;
  content: string;
  author: string;
  date: string;
  category: string;
  tags: string[];
  image?: string;
  readTime: number;
}

// Mock blog posts - in production, fetch from API
const BLOG_POSTS: BlogPost[] = [
  {
    id: '1',
    title: 'How AI Agents Are Transforming Software Development',
    slug: 'ai-agents-software-development',
    excerpt: 'Discover how intelligent AI agents are revolutionizing the way software is built, tested, and deployed.',
    content: `# How AI Agents Are Transforming Software Development

AI agents are no longer science fiction. They're here, and they're fundamentally changing how we build software.

## The Problem with Traditional Development

Traditional software development is resource-intensive:
- Developers spend hours on repetitive tasks
- Code reviews are manual and slow
- Testing is expensive and time-consuming
- Documentation lags behind code changes

## Enter AI Agents

Our swarm of AI agents changes this paradigm:

### 1. Faster Development
AI agents can write boilerplate code in seconds, freeing your team for creative work.

### 2. Better Quality
Automated testing and review catch issues before humans do.

### 3. Lower Costs
With agents handling routine tasks, you need fewer developers for the same output.

### 4. 24/7 Availability
Agents never sleep. Your development never stops.

## Real-World Impact

Companies using AI agent swarms report:
- 40% faster feature delivery
- 60% reduction in bugs
- 50% lower development costs
- 3x faster time-to-market

## The Future is Now

The companies that adopt AI agents today will dominate their markets tomorrow.

Are you ready to transform your development process?`,
    author: 'TitanForge Team',
    date: '2026-02-15',
    category: 'AI Development',
    tags: ['AI', 'Agents', 'Development', 'Automation'],
    readTime: 8,
  },
  {
    id: '2',
    title: 'The Economics of AI-as-a-Service',
    slug: 'economics-aia-as-a-service',
    excerpt: 'Why AI-as-a-Service is the fastest-growing software market segment and how to capitalize on it.',
    content: `# The Economics of AI-as-a-Service

The AI services market is growing 47% year-over-year. Here's why, and how you can profit.

## Market Opportunity

- Market size: $50B+ globally
- Growth rate: 47% YoY
- Projected by 2030: $500B+

This is the biggest software opportunity in decades.

## Why AI-as-a-Service Works

1. **Low Barrier to Entry**: Start with one service, scale to many
2. **High Margins**: Software has 70-80% gross margins
3. **Recurring Revenue**: Subscriptions = predictable income
4. **Network Effects**: More customers = better data = better service

## Business Models

### 1. Subscription-Based
Monthly/annual recurring revenue. Perfect for predictable cash flow.

### 2. Consumption-Based  
Pay per use. Aligns with customer value.

### 3. Hybrid
Fixed base + usage overage. Best of both worlds.

## Success Factors

- Product-market fit (understand your customers)
- Customer acquisition (sales & marketing)
- Retention (deliver value consistently)
- Operations (low-cost, high-volume)

## Getting Started

Start small, learn fast, scale aggressively. The winners in this space will be those who move fastest.`,
    author: 'TitanForge Team',
    date: '2026-02-10',
    category: 'Business',
    tags: ['SaaS', 'Business', 'Economics', 'Growth'],
    readTime: 6,
  },
  {
    id: '3',
    title: 'Building Your First AI Agent Swarm',
    slug: 'building-first-ai-agent-swarm',
    excerpt: 'A practical guide to creating your first AI agent swarm and putting it to work on real tasks.',
    content: `# Building Your First AI Agent Swarm

Creating an AI agent swarm is simpler than you think. Here's how to get started.

## What is an Agent Swarm?

A swarm is a collection of AI agents that work together to accomplish complex tasks. Each agent has specialized skills.

## The Four Essential Agents

1. **Strategist**: Plans the work
2. **Developer**: Executes technical tasks
3. **Reviewer**: Quality assurance
4. **Communicator**: Reports status

## Getting Started

1. Define your agents' roles
2. Set up communication channels
3. Create task workflows
4. Monitor and iterate

With TitanForge, this takes hours, not months.`,
    author: 'TitanForge Team',
    date: '2026-02-05',
    category: 'Tutorial',
    tags: ['Agents', 'Tutorial', 'Getting Started'],
    readTime: 5,
  },
];

export default function Blog() {
  const { slug } = useParams();
  const [posts, setPosts] = useState<BlogPost[]>(BLOG_POSTS);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  const categories = Array.from(new Set(posts.map(p => p.category)));
  const filteredPosts = selectedCategory 
    ? posts.filter(p => p.category === selectedCategory)
    : posts;

  if (slug) {
    const post = posts.find(p => p.slug === slug);
    if (!post) {
      return (
        <div className="container mx-auto px-4 py-12">
          <h1 className="text-2xl font-bold mb-4">Post Not Found</h1>
          <Link to="/blog" className="text-blue-600 hover:underline">Back to Blog</Link>
        </div>
      );
    }

    return (
      <div className="container mx-auto px-4 py-12">
        <article className="max-w-3xl mx-auto mb-12">
          <div className="mb-8">
            <div className="flex items-center gap-4 text-sm text-gray-600 mb-4">
              <span>{new Date(post.date).toLocaleDateString()}</span>
              <span>•</span>
              <span>{post.readTime} min read</span>
              <span>•</span>
              <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded">
                {post.category}
              </span>
            </div>

            <h1 className="text-4xl font-bold mb-4">{post.title}</h1>
            
            <div className="flex items-center gap-4 pb-4 border-b">
              <div>
                <p className="font-semibold text-gray-900">By {post.author}</p>
                <p className="text-sm text-gray-600">Published on {new Date(post.date).toLocaleDateString()}</p>
              </div>
            </div>
          </div>

          <div className="prose prose-lg max-w-none mb-8">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {post.content}
            </ReactMarkdown>
          </div>

          <div className="flex flex-wrap gap-2 pt-8 border-t">
            {post.tags.map(tag => (
              <span 
                key={tag}
                className="px-3 py-1 bg-gray-200 text-gray-700 rounded-full text-sm"
              >
                #{tag}
              </span>
            ))}
          </div>

          <div className="mt-12 p-6 bg-blue-50 rounded-lg">
            <h3 className="text-xl font-bold mb-2">Ready to transform your development?</h3>
            <p className="text-gray-700 mb-4">
              Join hundreds of companies using TitanForge to automate their software development.
            </p>
            <Link 
              to="/auth?tab=register"
              className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Start Your Free Trial
            </Link>
          </div>
        </article>

        <Link to="/blog" className="block mt-8 text-blue-600 hover:underline">
          ← Back to all posts
        </Link>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">TitanForge Blog</h1>
        <p className="text-xl text-gray-600 mb-8">
          Insights on AI, software development, and building scalable systems
        </p>
      </div>

      <div className="mb-8 flex flex-wrap gap-2">
        <button
          onClick={() => setSelectedCategory(null)}
          className={`px-4 py-2 rounded-full ${
            selectedCategory === null
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          All Posts
        </button>
        {categories.map(category => (
          <button
            key={category}
            onClick={() => setSelectedCategory(category)}
            className={`px-4 py-2 rounded-full ${
              selectedCategory === category
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            {category}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredPosts.map(post => (
          <Link
            key={post.id}
            to={`/blog/${post.slug}`}
            className="group border rounded-lg overflow-hidden hover:shadow-lg transition"
          >
            <div className="p-6">
              <div className="flex items-center gap-2 mb-3">
                <span className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded">
                  {post.category}
                </span>
                <span className="text-xs text-gray-500">
                  {new Date(post.date).toLocaleDateString()}
                </span>
              </div>
              
              <h3 className="text-xl font-bold mb-2 group-hover:text-blue-600">
                {post.title}
              </h3>
              
              <p className="text-gray-600 text-sm mb-4">{post.excerpt}</p>
              
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500">{post.readTime} min read</span>
                <span className="text-blue-600 group-hover:underline">Read More →</span>
              </div>
            </div>
          </Link>
        ))}
      </div>

      <div className="mt-16 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg p-12 text-center">
        <h2 className="text-3xl font-bold mb-4">Subscribe for Updates</h2>
        <p className="mb-6 text-blue-100">
          Get the latest insights on AI, development, and scaling delivered to your inbox
        </p>
      </div>
    </div>
  );
}
