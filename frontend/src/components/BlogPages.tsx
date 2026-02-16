import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import apiClient from '../services/api';

interface BlogPost {
  id: string;
  title: string;
  slug: string;
  content: string;
  excerpt?: string;
  author_id: string;
  tags?: string[];
  published: boolean;
  created_at: string;
  updated_at: string;
  featured_image_url?: string;
}

export const BlogList: React.FC = () => {
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        setLoading(true);
        const response = await apiClient.get('/api/v1/blog');
        setPosts(response.data);
      } catch (err) {
        setError('Failed to load blog posts');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <p className="text-gray-600">Loading blog posts...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="max-w-4xl mx-auto px-4 py-12"
    >
      <h1 className="text-4xl font-bold mb-8 text-center">Blog</h1>
      
      <div className="grid gap-6">
        {posts.length === 0 ? (
          <p className="text-center text-gray-600 py-12">No blog posts yet</p>
        ) : (
          posts.map((post) => (
            <Link key={post.id} to={`/blog/${post.slug}`}>
              <motion.article
                whileHover={{ scale: 1.02, boxShadow: '0 10px 25px rgba(0,0,0,0.1)' }}
                className="border rounded-lg p-6 hover:bg-gray-50 cursor-pointer transition"
              >
                <h2 className="text-2xl font-bold mb-2">{post.title}</h2>
                {post.excerpt && (
                  <p className="text-gray-600 mb-4">{post.excerpt}</p>
                )}
                <div className="flex items-center justify-between text-sm text-gray-500">
                  <span>{new Date(post.created_at).toLocaleDateString()}</span>
                  {post.tags && post.tags.length > 0 && (
                    <div className="flex gap-2">
                      {post.tags.map((tag) => (
                        <span key={tag} className="bg-blue-100 text-blue-800 px-2 py-1 rounded">
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </motion.article>
            </Link>
          ))
        )}
      </div>
    </motion.div>
  );
};

export const BlogDetail: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const [post, setPost] = useState<BlogPost | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPost = async () => {
      if (!slug) return;
      try {
        setLoading(true);
        const response = await apiClient.get(`/api/v1/blog/slug/${slug}`);
        setPost(response.data);
      } catch (err) {
        setError('Failed to load blog post');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchPost();
  }, [slug]);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <p className="text-gray-600">Loading blog post...</p>
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error || 'Blog post not found'}</p>
          <Link to="/blog" className="text-blue-600 hover:underline">
            Back to blog
          </Link>
        </div>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="max-w-3xl mx-auto px-4 py-12"
    >
      <Link to="/blog" className="text-blue-600 hover:underline mb-8 inline-block">
        ← Back to blog
      </Link>

      <article>
        <h1 className="text-4xl font-bold mb-4">{post.title}</h1>
        
        <div className="flex items-center gap-4 text-gray-600 mb-8 pb-8 border-b">
          <span>{new Date(post.created_at).toLocaleDateString()}</span>
          {post.tags && post.tags.length > 0 && (
            <div className="flex gap-2">
              {post.tags.map((tag) => (
                <span key={tag} className="bg-blue-100 text-blue-800 px-3 py-1 rounded text-sm">
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>

        {post.featured_image_url && (
          <img
            src={post.featured_image_url}
            alt={post.title}
            className="w-full h-96 object-cover rounded-lg mb-8"
          />
        )}

        <div className="prose prose-lg max-w-none">
          {/* Note: In production, use a markdown renderer like react-markdown */}
          <div dangerouslySetInnerHTML={{ __html: post.content }} />
        </div>

        {/* Call-to-action section */}
        <motion.div
          whileHover={{ scale: 1.02 }}
          className="mt-12 p-8 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg"
        >
          <h3 className="text-2xl font-bold mb-4">Ready to get started?</h3>
          <p className="mb-6">
            Experience the power of TitanForge AI agents today
          </p>
          <Link
            to="/signup"
            className="inline-block bg-white text-blue-600 font-bold px-6 py-3 rounded-lg hover:bg-gray-100 transition"
          >
            Start Free Trial
          </Link>
        </motion.div>
      </article>
    </motion.div>
  );
};
