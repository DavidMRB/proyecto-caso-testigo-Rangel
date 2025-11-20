import { CheckSquare } from 'lucide-react';

export default function Header() {
  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center gap-3">
          <CheckSquare className="text-indigo-600" size={32} />
          <div>
            <h1 className="text-2xl font-bold text-gray-800">
              Task Management System
            </h1>
            <p className="text-sm text-gray-600">
              Gestión empresarial de tareas con CI/CD
            </p>
          </div>
        </div>
      </div>
    </header>
  );
}