import React from 'react';

interface ScheduledJob {
    id: string;
    name: string;
    trigger: string;
    next_run_time: string;
}

interface SchedulerStatusPanelProps {
    jobs: ScheduledJob[];
}

const SchedulerStatusPanel: React.FC<SchedulerStatusPanelProps> = ({ jobs }) => {
    return (
        <div>
            {jobs.length === 0 ? (
                <p>No scheduled jobs found.</p>
            ) : (
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <thead>
                        <tr>
                            <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>ID</th>
                            <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Name</th>
                            <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Trigger</th>
                            <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Next Run Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        {jobs.map((job) => (
                            <tr key={job.id}>
                                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{job.id}</td>
                                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{job.name}</td>
                                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{job.trigger}</td>
                                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{job.next_run_time}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default SchedulerStatusPanel;
