import React from 'react';

interface Task {
  id: string;
  description: string;
  status: string;
  created_at: string;
  history: any[];
}

interface TaskDashboardProps {
  tasks: Task[];
}

const TaskDashboard: React.FC<TaskDashboardProps> = ({ tasks }) => {
  if (tasks.length === 0) {
    return <p>No tasks yet. Submit a goal to begin.</p>;
  }

  return (
    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
      <thead>
        <tr>
          <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>ID</th>
          <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Description</th>
          <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Status</th>
        </tr>
      </thead>
      <tbody>
        {tasks.map(task => (
          <tr key={task.id}>
            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{task.id.substring(0, 8)}...</td>
            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{task.description}</td>
            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{task.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default TaskDashboard;
