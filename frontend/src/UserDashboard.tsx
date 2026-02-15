import React from 'react';
import TaskDashboard from './TaskDashboard';
import SchedulerStatusPanel from './SchedulerStatusPanel'; // Assuming this component exists

interface UserDashboardProps {
    goal: string;
    setGoal: (goal: string) => void;
    response: string;
    setResponse: (response: string) => void;
    isRecording: boolean;
    setIsRecording: (isRecording: boolean) => void;
    tasks: any[];
    scheduledJobs: any[];
    handleSubmit: (e: React.FormEvent) => Promise<void>;
    handleVoiceInput: () => void;
}

const UserDashboard: React.FC<UserDashboardProps> = ({
    goal,
    setGoal,
    response,
    setResponse,
    isRecording,
    setIsRecording,
    tasks,
    scheduledJobs,
    handleSubmit,
    handleVoiceInput
}) => {
    return (
        <>
            <section style={{ marginBottom: '40px' }}>
                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                    <label htmlFor="goal" style={{ fontSize: '1.2em', fontWeight: 'bold' }}>
                        Submit a High-Level Goal for the Swarm:
                    </label>
                    <div style={{ position: 'relative', display: 'flex' }}>
                        <textarea
                            id="goal"
                            value={goal}
                            onChange={(e) => setGoal(e.target.value)}
                            placeholder="e.g., 'Develop a new marketing website for our company.'"
                            rows={5}
                            style={{ fontSize: '1em', padding: '10px', borderRadius: '5px', border: '1px solid #ccc', flexGrow: 1 }}
                        />
                        <button
                            type="button"
                            onClick={handleVoiceInput}
                            disabled={isRecording}
                            style={{
                                marginLeft: '10px',
                                padding: '10px',
                                cursor: 'pointer',
                                backgroundColor: isRecording ? '#dc3545' : '#28a745',
                                color: 'white',
                                border: 'none',
                                borderRadius: '5px'
                            }}
                            title="Speak Goal"
                        >
                            🎤
                        </button>
                    </div>
                    <button type="submit" style={{ padding: '10px 20px', fontSize: '1em', cursor: 'pointer', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '5px' }}>
                        Delegate to CEO
                    </button>
                </form>

                {response && (
                    <div style={{ marginTop: '30px', padding: '20px', backgroundColor: '#f0f0f0', borderRadius: '5px' }}>
                        <h3 style={{ marginTop: '0' }}>Last Response from MCP:</h3>
                        <pre>{response}</pre>
                    </div>
                )}
            </section>

            <section style={{ marginBottom: '40px' }}>
                <h2 style={{ borderBottom: '2px solid #ddd', paddingBottom: '10px' }}>Swarm Task Dashboard</h2>
                <TaskDashboard tasks={tasks} />
            </section>

            <section>
                <h2 style={{ borderBottom: '2px solid #ddd', paddingBottom: '10px' }}>Scheduler Status</h2>
                <SchedulerStatusPanel jobs={scheduledJobs} />
            </section>
        </>
    );
};

export default UserDashboard;
