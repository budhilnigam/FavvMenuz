export function formatCurrencyFromPaise(paise: number): string {
  const inr = paise / 100;
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(inr);
}

export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(amount);
}

export function formatDistance(distanceKm: number | null | undefined): string | null {
  if (distanceKm === null || distanceKm === undefined) return null;
  return `${distanceKm.toFixed(1)} km`;
}

export function getSpiceBadgeDetails(spice: string): { label: string; colorClass: string; iconCount: number } {
  switch (spice) {
    case 'extra_spicy':
      return { label: 'Extra Spicy', colorClass: 'bg-red-500 text-white border-black', iconCount: 3 };
    case 'spicy':
      return { label: 'Spicy', colorClass: 'bg-coral-500 text-white border-black', iconCount: 2 };
    case 'medium':
      return { label: 'Medium Spice', colorClass: 'bg-amber-400 text-black border-black', iconCount: 1 };
    case 'mild':
      return { label: 'Mild', colorClass: 'bg-emerald-400 text-black border-black', iconCount: 1 };
    case 'none':
    default:
      return { label: 'Not Spicy', colorClass: 'bg-gray-200 text-black border-black', iconCount: 0 };
  }
}

export function getDietaryTagStyle(tag: string): { label: string; bgClass: string; textClass: string } {
  switch (tag) {
    case 'jain_friendly':
      return { label: 'Jain Friendly', bgClass: 'bg-purple-100', textClass: 'text-purple-900 border-purple-900' };
    case 'vegetarian':
      return { label: 'Veg', bgClass: 'bg-green-100', textClass: 'text-green-900 border-green-900' };
    case 'vegan':
      return { label: 'Vegan', bgClass: 'bg-emerald-100', textClass: 'text-emerald-900 border-emerald-900' };
    case 'dairy_free':
      return { label: 'Dairy-Free', bgClass: 'bg-blue-100', textClass: 'text-blue-900 border-blue-900' };
    case 'gluten_free':
      return { label: 'Gluten-Free', bgClass: 'bg-amber-100', textClass: 'text-amber-900 border-amber-900' };
    default:
      return { label: tag.replace('_', ' '), bgClass: 'bg-gray-100', textClass: 'text-gray-900 border-gray-900' };
  }
}
