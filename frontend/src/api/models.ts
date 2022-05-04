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

export type SingleQAnswer = TextAnswer | MultipleChoiceAnswer

export interface FormAnswers
{
  formId: string
  answerId: string
  authorEmail: string
  answers: SingleQAnswer[]
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

export interface APIError<T>
{
  statusCode: number
  data: T
}

export interface HVEDetail
{
  loc: string | number
  msg: string
  type: string
}

export interface HTTPValidationError
{
  detail: HVEDetail[]
}
