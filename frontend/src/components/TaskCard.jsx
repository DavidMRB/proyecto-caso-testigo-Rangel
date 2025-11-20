import { useState } from 'react';
import { useTaskStore } from '../store/taskStore';
import { Edit2, Trash2, CheckCircle, Clock, AlertCircle } from 'lucide-react';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';
import TaskForm from './TaskForm';

const priorityColors = {
  low: 'bg-green-100 text-green-800',
  medium: 'bg-blue-100 text-blue-800',
  high: 'bg-orange-100 text-orange-800',
  urgent: 'bg-red-100 text-red-800'
};

const statusIcons = {
  pending: <Clock size={16} className="text-yellow-500" />,
  in_progress: <AlertCircle size={16} className="text-blue-500" />,
  completed: <CheckCircle size={16} className="text-green-500" />,
  cancelled: <Clock size={16} className="text-gray-500" />
};

export default function TaskCard({ task }) {
  const { deleteTask, updateTask } = useTaskStore();
  const [editing, setEditing] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const handleDelete = async () => {
    if (window.confirm('¿Estás seguro de eliminar esta tarea?')) {
      setDeleting(true);
      try {
        await deleteTask(task.id);
      } catch (error) {
        console.error('Error deleting task:', error);
        setDeleting(false);
      }
    }
  };

  const toggleStatus = async () => {
    const newStatus = task.status === 'completed' ? 'pending' : 'completed';
    await updateTask(task.id, { status: newStatus });
  };

  if (editing) {
    return <TaskForm task={task} onClose={() => setEditing(false)} />;
  }

  return (
    <div className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <button 
              onClick={toggleStatus}
              className="hover:scale-110 transition-transform"
            >
              {statusIcons[task.status]}
            </button>
            <h3 className={`text-lg font-semibold ${
              task.status === 'completed' ? 'line-through text-gray-500' : 'text-gray-800'
            }`}>
              {task.title}
            </h3>
            <span className={`px-2 py-1 rounded text-xs font-medium ${
              priorityColors[task.priority]
            }`}>
              {task.priority.toUpperCase()}
            </span>
          </div>

          {task.description && (
            <p className="text-gray-600 text-sm mb-3">{task.description}</p>
          )}

          <div className="flex flex-wrap gap-4 text-sm text-gray-500">
            {task.assigned_to && (
              <span>👤 {task.assigned_to}</span>
            )}
            {task.due_date && (
              <span>📅 {format(new Date(task.due_date), 'PPp', { locale: es })}</span>
            )}
            <span>Estado: {task.status.replace('_', ' ')}</span>
          </div>
        </div>

        <div className="flex gap-2 ml-4">
          <button
            onClick={() => setEditing(true)}
            className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
            title="Editar"
          >
            <Edit2 size={18} />
          </button>
          <button
            onClick={handleDelete}
            disabled={deleting}
            className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors
                     disabled:opacity-50"
            title="Eliminar"
          >
            <Trash2 size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}