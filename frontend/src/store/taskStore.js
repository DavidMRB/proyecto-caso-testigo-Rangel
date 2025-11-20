import { create } from 'zustand';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const useTaskStore = create((set, get) => ({
  tasks: [],
  loading: false,
  error: null,
  filters: {
    status: null,
    priority: null,
    search: ''
  },

  // Fetch all tasks
  fetchTasks: async () => {
    set({ loading: true, error: null });
    try {
      const { status, priority } = get().filters;
      const params = {};
      if (status) params.status = status;
      if (priority) params.priority = priority;

      const response = await axios.get(`${API_URL}/tasks`, { params });
      set({ tasks: response.data, loading: false });
    } catch (error) {
      set({ 
        error: error.response?.data?.detail || 'Error al cargar tareas',
        loading: false 
      });
    }
  },

  // Create new task
  createTask: async (taskData) => {
    set({ loading: true, error: null });
    try {
      const response = await axios.post(`${API_URL}/tasks`, taskData);
      set(state => ({ 
        tasks: [response.data, ...state.tasks],
        loading: false 
      }));
      return response.data;
    } catch (error) {
      set({ 
        error: error.response?.data?.detail || 'Error al crear tarea',
        loading: false 
      });
      throw error;
    }
  },

  // Update task
  updateTask: async (taskId, updates) => {
    set({ loading: true, error: null });
    try {
      const response = await axios.put(`${API_URL}/tasks/${taskId}`, updates);
      set(state => ({
        tasks: state.tasks.map(task => 
          task.id === taskId ? response.data : task
        ),
        loading: false
      }));
      return response.data;
    } catch (error) {
      set({ 
        error: error.response?.data?.detail || 'Error al actualizar tarea',
        loading: false 
      });
      throw error;
    }
  },

  // Delete task
  deleteTask: async (taskId) => {
    set({ loading: true, error: null });
    try {
      await axios.delete(`${API_URL}/tasks/${taskId}`);
      set(state => ({
        tasks: state.tasks.filter(task => task.id !== taskId),
        loading: false
      }));
    } catch (error) {
      set({ 
        error: error.response?.data?.detail || 'Error al eliminar tarea',
        loading: false 
      });
      throw error;
    }
  },

  // Set filters
  setFilter: (filterType, value) => {
    set(state => ({
      filters: {
        ...state.filters,
        [filterType]: value
      }
    }));
    get().fetchTasks();
  },

  // Clear filters
  clearFilters: () => {
    set({
      filters: {
        status: null,
        priority: null,
        search: ''
      }
    });
    get().fetchTasks();
  },

  // Get filtered tasks (client-side search)
  getFilteredTasks: () => {
    const { tasks, filters } = get();
    if (!filters.search) return tasks;

    return tasks.filter(task =>
      task.title.toLowerCase().includes(filters.search.toLowerCase()) ||
      task.description?.toLowerCase().includes(filters.search.toLowerCase())
    );
  }
}));