'use client'

import { useState, useEffect } from 'react'

// ============================================
// 1. LANDING PAGE COMPONENT
// ============================================
export default function HomePage() {
  const [page, setPage] = useState('landing')
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return null
  }

  if (page === 'login') return <LoginPage setPage={setPage} />
  if (page === 'signup') return <SignupPage setPage={setPage} />
  if (page === 'dashboard') return <DashboardPage setPage={setPage} />

  return (
    <div className="min-h-screen bg-white">
      <nav className="fixed top-0 left-0 right-0 bg-white/80 backdrop-blur-sm border-b border-gray-100 z-50 px-4 py-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            AdForge
          </span>
          <div className="flex items-center gap-4">
            <button onClick={() => setPage('login')} className="text-gray-600 hover:text-gray-900">Sign In</button>
            <button onClick={() => setPage('signup')} className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
              Get Started
            </button>
          </div>
        </div>
      </nav>

      <section className="pt-32 pb-20 px-4 max-w-7xl mx-auto text-center">
        <h1 className="text-4xl sm:text-6xl font-bold text-gray-900 leading-tight">
          Generate Campaign Assets
          <br />
          <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            In Minutes, Not Weeks
          </span>
        </h1>
        <p className="mt-6 text-xl text-gray-500 max-w-2xl mx-auto">
          AI-powered creative generation for D2C brands. Instagram, Facebook, Google, LinkedIn, and Pinterest.
        </p>
        <button 
          onClick={() => setPage('signup')}
          className="mt-10 bg-blue-600 text-white px-8 py-4 rounded-xl text-lg font-semibold hover:bg-blue-700"
        >
          Start Free Trial →
        </button>
      </section>

      <footer className="bg-gray-900 text-gray-400 px-4 py-8 text-center mt-20">
        <p>© 2026 AdForge AI. All rights reserved.</p>
      </footer>
    </div>
  )
}

// ============================================
// 2. LOGIN PAGE
// ============================================
function LoginPage({ setPage }: { setPage: (page: string) => void }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault()
    setPage('dashboard')
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-lg p-8">
        <h1 className="text-3xl font-bold text-center bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">AdForge</h1>
        <p className="text-center text-gray-500 mt-2 mb-8">Sign in to your account</p>

        <form onSubmit={handleLogin} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="you@example.com"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="••••••••"
              required
            />
          </div>
          <button type="submit" className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700">
            Sign In
          </button>
          <p className="text-center text-sm text-gray-500">
            Don't have an account?{' '}
            <button onClick={() => setPage('signup')} className="text-blue-600 hover:underline">
              Sign up free
            </button>
          </p>
        </form>
      </div>
    </div>
  )
}

// ============================================
// 3. SIGNUP PAGE
// ============================================
function SignupPage({ setPage }: { setPage: (page: string) => void }) {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSignup = (e: React.FormEvent) => {
    e.preventDefault()
    setPage('dashboard')
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-8">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-lg p-8">
        <h1 className="text-3xl font-bold text-center bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">AdForge</h1>
        <p className="text-center text-gray-500 mt-2 mb-8">Start your free trial</p>

        <form onSubmit={handleSignup} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-gray-700">Full Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="John Doe"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="you@example.com"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="At least 8 characters"
              required
            />
          </div>
          <button type="submit" className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700">
            Start Free Trial
          </button>
          <p className="text-center text-sm text-gray-500">
            Already have an account?{' '}
            <button onClick={() => setPage('login')} className="text-blue-600 hover:underline">
              Sign in
            </button>
          </p>
        </form>
      </div>
    </div>
  )
}

// ============================================
// 4. DASHBOARD PAGE (UPDATED - Fetches briefs)
// ============================================
function DashboardPage({ setPage }: { setPage: (page: string) => void }) {
  const [showNewBrief, setShowNewBrief] = useState(false)
  const [briefs, setBriefs] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchBriefs = async () => {
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://adforce-mc49.onrender.com'
      const response = await fetch(`${API_URL}/api/briefs`)
      const data = await response.json()
      setBriefs(data.briefs || [])
    } catch (error) {
      console.error('Failed to fetch briefs:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchBriefs()
  }, [])

  if (showNewBrief) {
    return <NewBriefPage setShowNewBrief={setShowNewBrief} onSuccess={fetchBriefs} />
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b border-gray-200 px-4 py-4 flex justify-between items-center">
        <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          AdForge
        </span>
        <button 
          onClick={() => setPage('landing')}
          className="text-sm text-gray-500 hover:text-gray-900"
        >
          Logout
        </button>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-gray-500">Welcome back! Create a new campaign to get started.</p>
          </div>
          <button
            onClick={() => setShowNewBrief(true)}
            className="bg-blue-600 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-blue-700 w-full sm:w-auto"
          >
            + New Campaign Brief
          </button>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <p className="text-sm text-gray-500">Briefs</p>
            <p className="text-2xl font-bold">{briefs.length}</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <p className="text-sm text-gray-500">Creative DNA</p>
            <p className="text-2xl font-bold">0</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <p className="text-sm text-gray-500">Assets</p>
            <p className="text-2xl font-bold">0</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <p className="text-sm text-gray-500">Live Campaigns</p>
            <p className="text-2xl font-bold">0</p>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-4">
          <div className="bg-gradient-to-r from-blue-50 to-blue-100 p-6 rounded-xl border border-blue-200">
            <h3 className="font-semibold text-blue-900">Generate Creative DNA</h3>
            <p className="text-sm text-blue-700">AI-powered hooks and copy</p>
            <button 
              onClick={() => setShowNewBrief(true)}
              className="mt-3 bg-blue-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-700"
            >
              Start
            </button>
          </div>
          <div className="bg-gradient-to-r from-purple-50 to-purple-100 p-6 rounded-xl border border-purple-200">
            <h3 className="font-semibold text-purple-900">Publish to Channels</h3>
            <p className="text-sm text-purple-700">Push to social media</p>
            <button className="mt-3 bg-purple-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-purple-700">
              View Assets
            </button>
          </div>
          <div className="bg-gradient-to-r from-green-50 to-green-100 p-6 rounded-xl border border-green-200">
            <h3 className="font-semibold text-green-900">Analytics</h3>
            <p className="text-sm text-green-700">Track performance</p>
            <button className="mt-3 bg-green-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-green-700">
              View
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

// ============================================
// 5. NEW BRIEF PAGE (UPDATED - Calls onSuccess)
// ============================================
function NewBriefPage({ setShowNewBrief, onSuccess }: { setShowNewBrief: (show: boolean) => void; onSuccess?: () => void }) {
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    product_name: '',
    offer: '',
    target_audience: '',
    brand_voice: '',
  })
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setSuccess('')

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://adforce-mc49.onrender.com'
      
      console.log("Creating brief at:", API_URL + '/api/briefs')
      const briefResponse = await fetch(`${API_URL}/api/briefs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tenant_id: 'test-tenant',
          product_name: formData.product_name,
          product_description: '',
          offer: formData.offer,
          target_audience: formData.target_audience,
          brand_voice: { tone: formData.brand_voice || 'professional' }
        })
      })

      if (!briefResponse.ok) {
        const errorData = await briefResponse.json()
        throw new Error(errorData.detail || 'Failed to create brief')
      }

      const briefData = await briefResponse.json()
      console.log("Brief created:", briefData)

      console.log("Generating creative assets...")
      const generateResponse = await fetch(`${API_URL}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          brief_id: briefData.id,
          tenant_id: 'test-tenant',
          channels: ['instagram', 'facebook']
        })
      })

      if (!generateResponse.ok) {
        const errorData = await generateResponse.json()
        throw new Error(errorData.detail || 'Failed to generate assets')
      }

      const generateData = await generateResponse.json()
      console.log("Generation result:", generateData)

      setSuccess('✅ Campaign created successfully! AI is generating your assets.')
      
      // Refresh the dashboard
      if (onSuccess) onSuccess()
      
      setTimeout(() => {
        setShowNewBrief(false)
      }, 2000)

    } catch (err: any) {
      console.error("Error:", err)
      setError(err.message || 'Something went wrong. Make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b border-gray-200 px-4 py-4 flex items-center justify-between sticky top-0 z-10">
        <button onClick={() => setShowNewBrief(false)} className="text-gray-600 hover:text-gray-900">
          ← Back
        </button>
        <h1 className="font-semibold text-gray-900">New Campaign Brief</h1>
        <div className="w-16"></div>
      </div>

      <div className="max-w-3xl mx-auto px-4 py-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
              ❌ {error}
            </div>
          )}
          {success && (
            <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
              {success}
            </div>
          )}

          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h2 className="font-semibold text-gray-900 mb-4">Product Information</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Product Name *</label>
                <input
                  type="text"
                  value={formData.product_name}
                  onChange={(e) => setFormData({ ...formData, product_name: e.target.value })}
                  className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., Organic Protein Bars"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Offer *</label>
                <input
                  type="text"
                  value={formData.offer}
                  onChange={(e) => setFormData({ ...formData, offer: e.target.value })}
                  className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., 20% off first order"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Target Audience *</label>
                <input
                  type="text"
                  value={formData.target_audience}
                  onChange={(e) => setFormData({ ...formData, target_audience: e.target.value })}
                  className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., Fitness enthusiasts 25-40"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Brand Voice</label>
                <input
                  type="text"
                  value={formData.brand_voice}
                  onChange={(e) => setFormData({ ...formData, brand_voice: e.target.value })}
                  className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., Witty, Professional, Inspiring"
                />
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3.5 rounded-xl font-semibold hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? '⏳ Generating...' : '🚀 Generate Campaign Assets'}
          </button>
        </form>
      </div>
    </div>
  )
}