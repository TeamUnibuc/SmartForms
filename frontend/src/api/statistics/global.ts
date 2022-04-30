import { FormDescription } from "../models";

interface StatisticsRes {
  total_number_of_forms: number,
  total_number_of_entries: number
}

export const StatsGlobal = async(): Promise<StatisticsRes> =>
{
  const data = await fetch('/api/statistics/global')
  const content = await data.json();
  return content;
}
