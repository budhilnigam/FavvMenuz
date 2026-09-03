import React from 'react';
import { AlertCircle } from 'lucide-react';

export const NoticeBanner: React.FC = () => {
  return (
    <div className="bg-electric-yellow border-b-2 border-black py-1.5 px-4 text-xs font-bold uppercase tracking-wider text-black flex items-center justify-center gap-2 text-center">
      <AlertCircle className="w-4 h-4 shrink-0 stroke-[2.5]" />
      <span>
        SIMULATED DEMO DATA: Fictional restaurants, synthetic prices & demo ratings in Noida. Not real-world orders or listings.
      </span>
    </div>
  );
};
