import React from 'react';
import { SearchSuggestion } from '../../types/search';
import { Flame, Utensils, Sparkles, Pizza, Salad, IceCream } from 'lucide-react';

interface SuggestionChipsProps {
  suggestions: SearchSuggestion[];
  onSelect: (query: string) => void;
}

const ICON_MAP: Record<string, React.ReactNode> = {
  Flame: <Flame className="w-3.5 h-3.5 text-coral-500 fill-coral-500" />,
  Utensils: <Utensils className="w-3.5 h-3.5 text-black" />,
  Sparkles: <Sparkles className="w-3.5 h-3.5 text-amber-500" />,
  Pizza: <Pizza className="w-3.5 h-3.5 text-coral-500" />,
  Salad: <Salad className="w-3.5 h-3.5 text-emerald-600" />,
  IceCream: <IceCream className="w-3.5 h-3.5 text-pink-500" />,
};

export const SuggestionChips: React.FC<SuggestionChipsProps> = ({ suggestions, onSelect }) => {
  return (
    <div className="flex flex-wrap items-center gap-2 pt-2">
      <span className="text-xs font-black uppercase tracking-wider text-gray-500 mr-1">
        Try Prompts:
      </span>
      {suggestions.map((s) => (
        <button
          key={s.id}
          type="button"
          onClick={() => onSelect(s.query)}
          className="group inline-flex items-center gap-1.5 px-3 py-1 bg-white border-2 border-black font-bold text-xs shadow-brutal-sm hover:shadow-none hover:translate-x-[2px] hover:translate-y-[2px] hover:bg-electric-yellow transition-all"
        >
          {ICON_MAP[s.icon] || <Utensils className="w-3.5 h-3.5" />}
          <span>{s.label}</span>
        </button>
      ))}
    </div>
  );
};
