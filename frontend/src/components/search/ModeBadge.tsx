import React from 'react';
import { Sparkles, Cpu } from 'lucide-react';

interface ModeBadgeProps {
  mode: 'ai' | 'fallback';
}

export const ModeBadge: React.FC<ModeBadgeProps> = ({ mode }) => {
  if (mode === 'ai') {
    return (
      <div
        className="inline-flex items-center gap-1.5 px-3 py-1 bg-electric-yellow border-2 border-black font-extrabold text-xs uppercase tracking-wider shadow-brutal-sm text-black"
        title="Parsed via configured Bedrock LLM"
      >
        <Sparkles className="w-3.5 h-3.5 text-black" />
        <span>AI Interpreted</span>
      </div>
    );
  }

  return (
    <div
      className="inline-flex items-center gap-1.5 px-3 py-1 bg-cream-200 border-2 border-black font-extrabold text-xs uppercase tracking-wider shadow-brutal-sm text-gray-800"
      title="Parsed deterministically via local rule engine (No external LLM call)"
    >
      <Cpu className="w-3.5 h-3.5 text-gray-700" />
      <span>Deterministic Fallback</span>
    </div>
  );
};
