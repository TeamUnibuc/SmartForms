type Choice = string;

interface FormMultipleChoiceQuestion
{
  title: string,
  description: string,
  choices: Choice[],
}

interface FormTextQuestion
{
  title: string,
  description: string,
  maxAnswerLength: number,
}

type Question = FormMultipleChoiceQuestion | FormTextQuestion;

export interface FormDescription
{
  title: string,
  formID?: string,
  description: string,
  questions: Question[],
  canBeFilledOnline: boolean,
  needsToBeSignedInToSubmit: boolean,
}
