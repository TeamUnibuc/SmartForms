type Choice = string;

export interface TextAnswer
{
  content: string
}

export interface MultipleChoiceAnswer
{
  content: string
  index: number
}

export interface FormAnswers
{
  formId: string
  answerId: string
  authorEmail: string
  answers: (TextAnswer | MultipleChoiceAnswer)[]
}

export interface FormMultipleChoiceQuestion
{
  title: string,
  description: string,
  choices: Choice[],
}

export interface FormTextQuestion
{
  title: string,
  description: string,
  maxAnswerLength: number,
}

export type Question = FormMultipleChoiceQuestion | FormTextQuestion;



export interface FormDescription
{
  title: string,
  formId: string,
  description: string,
  questions: Question[],
  canBeFilledOnline: boolean,
  needsToBeSignedInToSubmit: boolean,
}
