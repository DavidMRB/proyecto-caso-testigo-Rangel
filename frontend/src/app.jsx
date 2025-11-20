import { useState, useEffect } from 'react';
import { CheckCircle, Circle, Clock, AlertCircle, Plus, Trash2, Edit2 } from 'lucide-react';
import { useTaskStore } from './store/taskStore';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';
import TaskFilters from './components/TaskFilters';
import TaskStats from './components/TaskStats';
import Header from './components/Header';

function App() {
  const { tasks, loading, error, fetchTasks } = useTaskStore();
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Header />
      
      <main className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Stats Dashboard */}
        <TaskStats tasks={tasks} />

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
          {/* Filters Sidebar */}
          <div className="lg:col-span-1">
            <TaskFilters />
            
            <button
              onClick={() => setShowForm(!showForm)}
              className="w-full mt-4 bg-indigo-600 text-white px-6 py-3 rounded-lg
                       hover:bg-indigo-700 transition-colors flex items-center justify-center gap-2
                       shadow-lg hover:shadow-xl"
            >
              <Plus size={20} />
              Nueva Tarea
            </button>

            {showForm && (
              <div className="mt-4">
                <TaskForm onClose={() => setShowForm(false)} />
              </div>
            )}
          </div>

          {/* Task List */}
          <div className="lg:col-span-2">
            {loading && (
              <div className="text-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
                <p className="mt-4 text-gray-600">Cargando tareas...</p>
              </div>
            )}

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
                <p className="text-red-800">Error: {error}</p>
              </div>
            )}

            {!loading && !error && <TaskList />}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-16 py-6 bg-white border-t border-gray-200">
        <div className="container mx-auto px-4 text-center text-gray-600">
          <p>Task Management System v1.0.0 - CI/CD Project</p>
        </div>
      </footer>
    </div>
  );
}

export default App;