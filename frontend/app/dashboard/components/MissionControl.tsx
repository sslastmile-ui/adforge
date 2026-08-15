'use client';

import { useEffect, useState } from 'react';

type AgentStatus = 'running' | 'idle' | 'completed' | 'error';

type Agent = {
  agent: string;
  status: AgentStatus;
  task: string;
};

const DEFAULT_AGENTS: Agent[] = [
  {
    agent: 'AI CEO',
    status: 'running',
    task: 'Strategic planning',
  },
  {
    agent: 'AI CMO',
    status: 'running',
    task: 'Campaign optimization',
  },
  {
    agent: 'AI CFO',
    status: 'idle',
    task: 'Budget review',
  },
];

function getStatusClasses(status: AgentStatus): string {
  switch (status) {
    case 'running':
      return 'bg-green-100 text-green-700';

    case 'completed':
      return 'bg-blue-100 text-blue-700';

    case 'error':
      return 'bg-red-100 text-red-700';

    case 'idle':
    default:
      return 'bg-gray-100 text-gray-600';
  }
}

export default function MissionControl() {
  const [agents, setAgents] = useState<Agent[]>(DEFAULT_AGENTS);

  useEffect(() => {
    setAgents(DEFAULT_AGENTS);
  }, []);

  return (
    <section className="w-full rounded-xl border bg-white p-6 shadow-sm">
      <div className="mb-5">
        <h2 className="text-xl font-semibold text-gray-900">
          Mission Control
        </h2>

        <p className="mt-1 text-sm text-gray-500">
          AI agents and current business operations
        </p>
      </div>

      <div className="space-y-3">
        {agents.map((agent, index) => (
          <div
            key={`${agent.agent}-${index}`}
            className="flex items-center justify-between rounded-lg border border-gray-200 p-4"
          >
            <div>
              <div className="font-medium text-gray-900">
                {agent.agent}
              </div>

              <div className="mt-1 text-sm text-gray-500">
                {agent.task}
              </div>
            </div>

            <span
              className={`rounded-full px-3 py-1 text-xs font-medium ${getStatusClasses(
                agent.status,
              )}`}
            >
              {agent.status}
            </span>
          </div>
        ))}
      </div>

      <div className="mt-5 rounded-lg bg-gray-50 p-4 text-sm text-gray-600">
        2 opportunities detected. Review recommended.
      </div>
    </section>
  );
}
