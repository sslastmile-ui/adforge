'use client'

import { useState, useEffect } from 'react'

export default function HomePage() {
  const [page, setPage] = useState('landing')
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null

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
// 4. DASHBOARD PAGE - SIDE NAV LAYOUT (Like OrbitR)
// ============================================
function DashboardPage({ setPage }: { setPage: (page: string) => void }) {
  const [showNewBrief, setShowNewBrief] = useState(false)
  const [briefs, setBriefs] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('campaigns')

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://adforce-mc49.onrender.com'

  const fetchBriefs = async () => {
    try {
      const response = await fetch(`${API_URL}/api/briefs/`)
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

  const briefsWithDNA = briefs.filter((b: any) => b.dna && b.dna.hook).length

  // Sidebar Navigation Items
  const navItems = [
    { id: 'campaigns', label: 'Campaigns', icon: '📊' },
    { id: 'creative', label: 'Creative DNA', icon: '🧬' },
    { id: 'assets', label: 'Channel Assets', icon: '📱' },
    { id: 'analytics', label: 'Analytics', icon: '📈' },
    { id: 'settings', label: 'Settings', icon: '⚙️' },
  ]

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar - Like OrbitR */}
      <div className="w-64 bg-white border-r border-gray-200 fixed top-0 left-0 bottom-0 overflow-y-auto">
        <div className="p-6 border-b border-gray-100">
          <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            AdForge
          </span>
        </div>

        <nav className="p-4 space-y-1">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                activeTab === item.id
                  ? 'bg-blue-50 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <span className="mr-3">{item.icon}</span>
              {item.label}
            </button>
          ))}
          
          <hr className="my-4 border-gray-100" />
          
          <button 
            onClick={() => setPage('landing')}
            className="w-full flex items-center px-4 py-3 rounded-lg text-sm font-medium text-red-600 hover:bg-red-50 transition-colors"
          >
            <span className="mr-3">🚪</span>
            Logout
          </button>
        </nav>
      </div>

      {/* Main Content */}
      <div className="ml-64 flex-1">
        {/* Top Bar */}
        <div className="bg-white border-b border-gray-200 px-8 py-4 flex justify-between items-center sticky top-0 z-10">
          <div>
            <h1 className="text-xl font-semibold text-gray-900">Campaigns</h1>
            <p className="text-sm text-gray-500">Manage your AI-generated marketing campaigns</p>
          </div>
          <button
            onClick={() => setShowNewBrief(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors flex items-center"
          >
            <span className="mr-2">+</span>
            New Campaign
          </button>
        </div>

        {/* Stats Cards */}
        <div className="px-8 pt-6 grid grid-cols-4 gap-4">
          <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
            <p className="text-xs text-gray-500 uppercase tracking-wider">Total Campaigns</p>
            <p className="text-2xl font-bold">{briefs.length}</p>
          </div>
          <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
            <p className="text-xs text-gray-500 uppercase tracking-wider">Creative DNA</p>
            <p className="text-2xl font-bold">{briefsWithDNA}</p>
          </div>
          <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
            <p className="text-xs text-gray-500 uppercase tracking-wider">Assets Ready</p>
            <p className="text-2xl font-bold">{briefsWithDNA * 2}</p>
          </div>
          <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
            <p className="text-xs text-gray-500 uppercase tracking-wider">Live</p>
            <p className="text-2xl font-bold">0</p>
          </div>
        </div>

        {/* Campaigns Grid */}
        <div className="px-8 py-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-sm font-medium text-gray-700">All Campaigns</h2>
            <span className="text-xs text-gray-400">{briefs.length} campaigns</span>
          </div>

          {briefs.length === 0 ? (
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-16 text-center">
              <div className="text-4xl mb-4">🚀</div>
              <p className="text-gray-500 font-medium">No campaigns yet</p>
              <p className="text-sm text-gray-400 mt-1">Create your first campaign to get started</p>
              <button
                onClick={() => setShowNewBrief(true)}
                className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg text-sm hover:bg-blue-700"
              >
                Create Campaign
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
              {briefs.map((brief: any) => (
                <div key={brief.id} className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow">
                  {/* Campaign Header */}
                  <div className="p-5 border-b border-gray-100 flex justify-between items-start">
                    <div>
                      <div className="flex items-center gap-2">
                        <h3 className="font-semibold text-gray-900">{brief.product_name}</h3>
                        <span className={`px-2 py-0.5 text-xs font-medium rounded-full ${
                          brief.status === 'approved' ? 'bg-green-100 text-green-700' :
                          brief.status === 'processing' ? 'bg-yellow-100 text-yellow-700' :
                          'bg-gray-100 text-gray-700'
                        }`}>
                          {brief.status || 'draft'}
                        </span>
                      </div>
                      <div className="flex items-center gap-4 mt-1">
                        <span className="text-xs text-gray-400">{brief.offer}</span>
                        <span className="text-xs text-gray-400">•</span>
                        <span className="text-xs text-gray-400">{brief.target_audience}</span>
                      </div>
                    </div>
                    <button className="text-gray-400 hover:text-gray-600">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                      </svg>
                    </button>
                  </div>

                  {/* DNA Content */}
                  <div className="p-5">
                    {brief.dna && brief.dna.hook ? (
                      <div className="space-y-3">
                        <div className="grid grid-cols-2 gap-3">
                          <div className="bg-blue-50 rounded-lg p-3 border border-blue-100">
                            <p className="text-xs font-medium text-blue-900 uppercase tracking-wider">Hook</p>
                            <p className="text-sm text-blue-800 mt-1">{brief.dna.hook}</p>
                          </div>
                          <div className="bg-purple-50 rounded-lg p-3 border border-purple-100">
                            <p className="text-xs font-medium text-purple-900 uppercase tracking-wider">Value Prop</p>
                            <p className="text-sm text-purple-800 mt-1">{brief.dna.value_prop}</p>
                          </div>
                        </div>
                        <div className="grid grid-cols-2 gap-3">
                          <div className="bg-green-50 rounded-lg p-3 border border-green-100">
                            <p className="text-xs font-medium text-green-900 uppercase tracking-wider">CTA</p>
                            <p className="text-sm text-green-800 mt-1">{brief.dna.cta}</p>
                          </div>
                          <div className="bg-yellow-50 rounded-lg p-3 border border-yellow-100">
                            <p className="text-xs font-medium text-yellow-900 uppercase tracking-wider">Visual</p>
                            <p className="text-sm text-yellow-800 mt-1">{brief.dna.visual_sentiment}</p>
                          </div>
                        </div>

                        <div className="flex flex-wrap gap-2 pt-2">
                          <span className="px-3 py-1 bg-pink-100 text-pink-700 text-xs rounded-full">Instagram</span>
                          <span className="px-3 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">Facebook</span>
                          <span className="px-3 py-1 bg-green-100 text-green-700 text-xs rounded-full">Google</span>
                          <span className="px-3 py-1 bg-red-100 text-red-700 text-xs rounded-full">LinkedIn</span>
                          <span className="px-3 py-1 bg-orange-100 text-orange-700 text-xs rounded-full">Pinterest</span>
                        </div>
                      </div>
                    ) : (
                      <div className="text-center py-6">
                        <div className="animate-pulse flex flex-col items-center">
                          <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                          <p className="text-sm text-gray-400 mt-2">AI generating creative DNA...</p>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Footer Actions */}
                  <div className="bg-gray-50 px-5 py-3 border-t border-gray-100 flex justify-between items-center">
                    <span className="text-xs text-gray-400">
                      {new Date(brief.created_at).toLocaleDateString()}
                    </span>
                    <div className="flex gap-3">
                      <button className="text-xs text-gray-500 hover:text-gray-700 font-medium">Edit</button>
                      <button className="text-xs text-blue-600 hover:text-blue-800 font-medium">Publish</button>
                      <button className="text-xs text-gray-400 hover:text-gray-600 font-medium">Duplicate</button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

// ============================================
// 5. NEW BRIEF PAGE
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

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://adforce-mc49.onrender.com'

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setSuccess('')

    try {
      const briefResponse = await fetch(`${API_URL}/api/briefs/`, {
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

      const generateResponse = await fetch(`${API_URL}/api/generate/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          brief_id: briefData.id,
          tenant_id: 'test-tenant',
          channels: ['instagram', 'facebook', 'google', 'linkedin', 'pinterest']
        })
      })

      if (!generateResponse.ok) {
        const errorData = await generateResponse.json()
        throw new Error(errorData.detail || 'Failed to generate assets')
      }

      setSuccess('✅ Campaign created successfully! AI is generating content.')

      if (onSuccess) onSuccess()

      setTimeout(() => {
        setShowNewBrief(false)
      }, 2000)

    } catch (err: any) {
      console.error("Error:", err)
      setError(err.message || 'Something went wrong.')
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