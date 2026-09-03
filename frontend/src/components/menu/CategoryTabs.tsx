import React from 'react';

interface CategoryTabsProps {
  categories: string[];
  selectedCategory: string;
  onSelectCategory: (category: string) => void;
}

export const CategoryTabs: React.FC<CategoryTabsProps> = ({
  categories,
  selectedCategory,
  onSelectCategory,
}) => {
  return (
    <div className="flex flex-wrap gap-2">
      {categories.map((cat) => (
        <button
          key={cat}
          type="button"
          onClick={() => onSelectCategory(cat)}
          className={`px-3.5 py-1.5 border-2 border-black font-extrabold text-xs tracking-wide transition-all ${
            selectedCategory === cat
              ? 'bg-electric-yellow shadow-brutal-sm -translate-y-0.5'
              : 'bg-white hover:bg-cream-100'
          }`}
        >
          {cat}
        </button>
      ))}
    </div>
  );
};
