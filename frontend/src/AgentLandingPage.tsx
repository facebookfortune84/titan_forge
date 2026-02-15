import React from 'react';

interface AgentLandingPageProps {
  htmlContent: string;
}

const AgentLandingPage: React.FC<AgentLandingPageProps> = ({ htmlContent }) => {
  return (
    <div className="agent-landing-page">
      {htmlContent ? (
        <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
      ) : (
        <p>No landing page content available yet. Agents are working on it!</p>
      )}
    </div>
  );
};

export default AgentLandingPage;
