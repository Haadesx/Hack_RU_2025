import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  ArrowLeft, 
  Mic, 
  Heart, 
  Activity, 
  Moon, 
  Sun, 
  TrendingUp, 
  Calendar,
  Settings,
  Download,
  Share2
} from 'lucide-react'
import { useWellness } from '../context/WellnessContext'

function Dashboard() {
  const navigate = useNavigate()
  const { state } = useWellness()
  
  const [selectedTab, setSelectedTab] = useState('overview')
  
  // Mock historical data for demo
  const mockHistory = [
    { date: '2024-01-15', stress: 0.3, energy: 0.7, sleep: 8.5 },
    { date: '2024-01-14', stress: 0.6, energy: 0.5, sleep: 7.2 },
    { date: '2024-01-13', stress: 0.4, energy: 0.8, sleep: 8.0 },
    { date: '2024-01-12', stress: 0.7, energy: 0.4, sleep: 6.5 },
    { date: '2024-01-11', stress: 0.5, energy: 0.6, sleep: 7.8 },
  ]
  
  const tabs = [
    { id: 'overview', label: 'Overview', icon: Activity },
    { id: 'history', label: 'History', icon: Calendar },
    { id: 'insights', label: 'Insights', icon: TrendingUp },
    { id: 'settings', label: 'Settings', icon: Settings }
  ]
  
  const renderOverview = () => (
    <div className="space-y-6">
      {/* Current Status */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Current Wellness Status</h3>
        <div className="grid md:grid-cols-3 gap-4">
          <div className="text-center p-4 bg-red-50 rounded-lg">
            <Heart className="w-8 h-8 text-red-500 mx-auto mb-2" />
            <div className="text-2xl font-bold text-red-600">
              {state.audioFeatures ? (state.audioFeatures.stress_score * 100).toFixed(0) : '--'}%
            </div>
            <div className="text-sm text-gray-600">Stress Level</div>
          </div>
          
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <Activity className="w-8 h-8 text-blue-500 mx-auto mb-2" />
            <div className="text-2xl font-bold text-blue-600">
              {state.audioFeatures ? (state.audioFeatures.energy * 100).toFixed(0) : '--'}%
            </div>
            <div className="text-sm text-gray-600">Energy Level</div>
          </div>
          
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <Moon className="w-8 h-8 text-green-500 mx-auto mb-2" />
            <div className="text-2xl font-bold text-green-600">8.2h</div>
            <div className="text-sm text-gray-600">Avg Sleep</div>
          </div>
        </div>
      </div>
      
      {/* Quick Actions */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid md:grid-cols-2 gap-4">
          <button
            onClick={() => navigate('/record')}
            className="btn-primary flex items-center justify-center space-x-2"
          >
            <Mic className="w-5 h-5" />
            <span>New Check-in</span>
          </button>
          
          <button className="btn-secondary flex items-center justify-center space-x-2">
            <Moon className="w-5 h-5" />
            <span>Sleep Hypnosis</span>
          </button>
        </div>
      </div>
      
      {/* Recent Insights */}
      {state.insights && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Latest Insights</h3>
          <div className="prose max-w-none">
            <p className="text-gray-700 leading-relaxed">
              {state.insights.narrative}
            </p>
          </div>
          
          {state.insights.action_items && (
            <div className="mt-4">
              <h4 className="font-medium text-gray-900 mb-2">Action Items:</h4>
              <ul className="space-y-2">
                {state.insights.action_items.slice(0, 3).map((item, index) => (
                  <li key={index} className="flex items-start space-x-2">
                    <div className="w-2 h-2 bg-primary-500 rounded-full mt-2 flex-shrink-0"></div>
                    <span className="text-gray-700">{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
  
  const renderHistory = () => (
    <div className="space-y-6">
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Wellness Trends</h3>
        <div className="space-y-4">
          {mockHistory.map((entry, index) => (
            <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-4">
                <Calendar className="w-5 h-5 text-gray-500" />
                <span className="font-medium text-gray-900">{entry.date}</span>
              </div>
              
              <div className="flex items-center space-x-6">
                <div className="text-center">
                  <div className="text-sm font-medium text-red-600">
                    {(entry.stress * 100).toFixed(0)}%
                  </div>
                  <div className="text-xs text-gray-500">Stress</div>
                </div>
                
                <div className="text-center">
                  <div className="text-sm font-medium text-blue-600">
                    {(entry.energy * 100).toFixed(0)}%
                  </div>
                  <div className="text-xs text-gray-500">Energy</div>
                </div>
                
                <div className="text-center">
                  <div className="text-sm font-medium text-green-600">
                    {entry.sleep}h
                  </div>
                  <div className="text-xs text-gray-500">Sleep</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
  
  const renderInsights = () => (
    <div className="space-y-6">
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Wellness Patterns</h3>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Stress Patterns</h4>
            <p className="text-gray-600 text-sm">
              Your stress levels tend to be higher in the afternoon and lower in the morning. 
              Consider scheduling demanding tasks earlier in the day.
            </p>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Energy Optimization</h4>
            <p className="text-gray-600 text-sm">
              Your energy peaks around 10 AM and dips after 2 PM. 
              Plan breaks and lighter activities during low-energy periods.
            </p>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Sleep Quality</h4>
            <p className="text-gray-600 text-sm">
              Consistent sleep schedule improves your overall wellness scores. 
              Aim for 7-9 hours of sleep for optimal recovery.
            </p>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Voice Analysis</h4>
            <p className="text-gray-600 text-sm">
              Your speaking rate and pitch patterns indicate good emotional regulation. 
              Continue practicing mindfulness techniques.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
  
  const renderSettings = () => (
    <div className="space-y-6">
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Preferences</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Voice Selection
            </label>
            <select className="input-field">
              <option value="alloy">Alloy (Default)</option>
              <option value="echo">Echo</option>
              <option value="fable">Fable</option>
              <option value="onyx">Onyx</option>
              <option value="nova">Nova</option>
              <option value="shimmer">Shimmer</option>
            </select>
          </div>
          
          <div className="flex items-center justify-between">
            <div>
              <label className="text-sm font-medium text-gray-700">
                Daily Reminders
              </label>
              <p className="text-xs text-gray-500">
                Get notified to do wellness check-ins
              </p>
            </div>
            <input type="checkbox" className="rounded" defaultChecked />
          </div>
          
          <div className="flex items-center justify-between">
            <div>
              <label className="text-sm font-medium text-gray-700">
                Privacy Mode
              </label>
              <p className="text-xs text-gray-500">
                Keep all data local, no cloud processing
              </p>
            </div>
            <input type="checkbox" className="rounded" />
          </div>
        </div>
      </div>
      
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Data Management</h3>
        <div className="space-y-3">
          <button className="btn-secondary w-full flex items-center justify-center space-x-2">
            <Download className="w-4 h-4" />
            <span>Export Data</span>
          </button>
          
          <button className="btn-secondary w-full flex items-center justify-center space-x-2">
            <Share2 className="w-4 h-4" />
            <span>Share Insights</span>
          </button>
        </div>
      </div>
    </div>
  )
  
  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <button
          onClick={() => navigate('/analysis')}
          className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>Back</span>
        </button>
        
        <h1 className="text-2xl font-bold text-gray-900">Wellness Dashboard</h1>
        
        <div className="w-20"></div> {/* Spacer */}
      </div>
      
      {/* Tabs */}
      <div className="border-b border-gray-200 mb-8">
        <nav className="flex space-x-8">
          {tabs.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setSelectedTab(id)}
              className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                selectedTab === id
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{label}</span>
            </button>
          ))}
        </nav>
      </div>
      
      {/* Tab Content */}
      {selectedTab === 'overview' && renderOverview()}
      {selectedTab === 'history' && renderHistory()}
      {selectedTab === 'insights' && renderInsights()}
      {selectedTab === 'settings' && renderSettings()}
    </div>
  )
}

export default Dashboard