import { FaClock, FaBolt, FaCheckCircle } from 'react-icons/fa'

function ActionItems({ items }) {
  if (!items || items.length === 0) {
    return null
  }

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 1:
        return 'border-red-300 bg-red-50'
      case 2:
        return 'border-yellow-300 bg-yellow-50'
      case 3:
        return 'border-green-300 bg-green-50'
      default:
        return 'border-blue-300 bg-blue-50'
    }
  }

  const getPriorityLabel = (priority) => {
    switch (priority) {
      case 1:
        return { text: 'Do Now', icon: '🔴' }
      case 2:
        return { text: 'Today', icon: '🟡' }
      case 3:
        return { text: 'This Week', icon: '🟢' }
      default:
        return { text: 'Suggested', icon: '🔵' }
    }
  }

  return (
    <div className="card">
      <h3 className="text-2xl font-semibold mb-6 flex items-center space-x-2">
        <FaCheckCircle className="text-blue-600" />
        <span>Your Action Plan</span>
      </h3>

      <div className="space-y-4">
        {items.map((item, idx) => {
          const priority = item.priority || idx + 1
          const priorityInfo = getPriorityLabel(priority)
          
          return (
            <div
              key={idx}
              className={`border-2 rounded-xl p-5 ${getPriorityColor(priority)} hover:shadow-md transition-shadow`}
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <span className="text-2xl">{priorityInfo.icon}</span>
                    <span className="text-xs font-semibold uppercase tracking-wide text-gray-600">
                      {priorityInfo.text}
                    </span>
                  </div>
                  <h4 className="text-lg font-semibold text-gray-900">
                    {item.title}
                  </h4>
                </div>
              </div>

              {/* Description */}
              <p className="text-gray-700 mb-4 leading-relaxed">
                {item.description}
              </p>

              {/* Meta Information */}
              <div className="flex items-center space-x-6 text-sm">
                {item.estimated_time && (
                  <div className="flex items-center space-x-2 text-gray-600">
                    <FaClock className="text-blue-500" />
                    <span>{item.estimated_time}</span>
                  </div>
                )}
                
                {item.impact && (
                  <div className="flex items-center space-x-2 text-gray-600">
                    <FaBolt className="text-yellow-500" />
                    <span className="text-xs">{item.impact}</span>
                  </div>
                )}
              </div>

              {/* Optional: Add a "Mark Complete" button for interactivity */}
              {priority === 1 && (
                <button
                  className="mt-4 w-full py-2 bg-white border-2 border-gray-300 rounded-lg 
                           hover:bg-gray-50 transition-colors text-sm font-medium"
                  onClick={() => {
                    // Could integrate with a todo system or just provide visual feedback
                    alert(`Great! Take a moment to: ${item.title}`)
                  }}
                >
                  Start Now
                </button>
              )}
            </div>
          )
        })}
      </div>

      {/* Breathing Exercise Call-out */}
      <div className="mt-6 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border-2 border-blue-200">
        <div className="flex items-center space-x-3">
          <div className="breathe-circle flex-shrink-0 w-12 h-12"></div>
          <div>
            <p className="font-semibold text-gray-900">Remember to breathe</p>
            <p className="text-sm text-gray-600">
              Even 2 minutes of focused breathing can reset your nervous system
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ActionItems
