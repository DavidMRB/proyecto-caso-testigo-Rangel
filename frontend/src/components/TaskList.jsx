import { useTaskStore } from '../store/taskStore';
import TaskCard from './TaskCard';

export default function TaskList() {
  const { getFilteredTasks } = useTaskStore();
  const tasks = getFilteredTasks();

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12 bg-white rounded-lg shadow">
        <p className="text-gray-500 text-lg">No hay tareas disponibles</p>
        <p className="text-gray-400 text-sm mt-2">
          Crea una nueva tarea para comenzar
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {tasks.map(task => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  );
}