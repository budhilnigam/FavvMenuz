import React, { useState } from 'react';
import { Search, Loader2, X } from 'lucide-react';

interface SearchBarProps {
  initialQuery?: string;
  onSearch: (query: string) => void;
  isLoading?: boolean;
  placeholder?: string;
  autoFocus?: boolean;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  initialQuery = '',
  onSearch,
  isLoading = false,
  placeholder = 'e.g. Spicy vegetarian food under ₹350 near Sector 62...',
  autoFocus = false,
}) => {
  const [inputVal, setInputVal] = useState(initialQuery);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputVal.trim()) {
      onSearch(inputVal.trim());
    }
  };

  const handleClear = () => {
    setInputVal('');
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="relative flex flex-col sm:flex-row items-stretch gap-2">
        <div className="relative flex-1">
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-black">
            <Search className="h-6 w-6 stroke-[2.5]" />
          </div>
          <input
            type="text"
            value={inputVal}
            onChange={(e) => setInputVal(e.target.value)}
            placeholder={placeholder}
            autoFocus={autoFocus}
            className="w-full pl-12 pr-10 py-3.5 bg-white border-3 border-black text-ink font-bold text-base sm:text-lg shadow-brutal placeholder:text-gray-400 placeholder:font-normal focus:bg-yellow-50/30 transition-all"
          />
          {inputVal && (
            <button
              type="button"
              onClick={handleClear}
              className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-gray-500 hover:text-black"
            >
              <X className="h-5 w-5" />
            </button>
          )}
        </div>
        <button
          type="submit"
          disabled={isLoading || !inputVal.trim()}
          className="btn-brutal text-base sm:text-lg flex items-center justify-center gap-2 px-8 py-3.5 shrink-0"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Thinking...</span>
            </>
          ) : (
            <>
              <span>Find Dishes</span>
              <span className="font-mono text-sm hidden sm:inline">↵</span>
            </>
          )}
        </button>
      </div>
    </form>
  );
};
