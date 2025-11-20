import { CheckCircle, Clock, AlertCircle, TrendingUp } from 'lucide-react';

export default function TaskStats({ tasks }) {
  const stats = {
    total: tasks.length,
    completed: tasks.filter(t => t.status === 'completed').length,
    pending: tasks.filter(t => t.status === 'pending').length,
    inProgress: tasks.filter(t => t.status === 'in_progress').length
  };

  const completionRate = stats.total > 0 
    ? Math.round((stats.completed / stats.total) * 100) 
    : 0;

  const statCards = [
    { label: 'Total', value: stats.total, icon: TrendingUp, color: 'bg-blue-500' },
    { label: 'Completadas', value: stats.completed, icon: CheckCircle, color: 'bg-green-500' },
    { label: 'En Progreso', value: stats.inProgress, icon: AlertCircle, color: 'bg-orange-500' },
    { label: 'Pendientes', value: stats.pending, icon: Clock, color: 'bg-yellow-500' }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {statCards.map(({ label, value, icon: Icon, color }) => (
        <div key={label} className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">{label}</p>
              <p className="text-3xl font-bold text-gray-800 mt-1">{value}</p>
            </div>
            <div className={`${color} p-3 rounded-full`}>
              <Icon className="text-white" size={24} />
            </div>
          </div>
          {label === 'Completadas' && (
            <div className="mt-3 pt-3 border-t border-gray-200">
              <p className="text-sm text-gray-600">
                Tasa de completitud: <span className="font-semibold">{completionRate}%</span>
              </p>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}