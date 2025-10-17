// Демо утилиты для показа Git workflow

export const formatDemoData = (data: any) => {
  return `Demo: ${JSON.stringify(data)}`;
};

export const calculateDemoMetric = (value: number) => {
  return value * 1.5;
};
