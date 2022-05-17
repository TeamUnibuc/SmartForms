import React from "react"

import { createContext, useContext, useState } from "react";
import { Question } from "~/api/models";

interface QLUpdaterType {
  qOps: {
    setQuestion: (q_ind: number, q: Question) => void
    addQuestion: (q: Question | undefined) => void
    delQuestion: (index?: number) => void
  }
  sOps: {
    setPdfString: (base64: string) => void
  }
  dOps: {
    setTitle: (t: string) => void
    setDesc: (d: string) => void
    setFillOnline: (x: boolean) => void
    setSigndSubmit: (x: boolean) => void
  }
}

interface QLStateType {
  qList: {
    questions: (Question | undefined)[]
  },
  title: string
  description: string
  canBeFilledOnline: boolean
  needsToBeSignedInToSubmit: boolean
  pdfString: string
}

// create contexts
const QLContextState = createContext<undefined | QLStateType>(undefined);
const QLContextUpdater = createContext<undefined | QLUpdaterType>(undefined);

// context consumer hook
const useQLContextState = () => {
  // get the context
  const context = useContext(QLContextState);

  // if `undefined`, throw an error
  if (context === undefined) {
    throw new Error("useQLContextState was used outside of its Provider");
  }

  return context;
};

// context consumer hook
const useQLContextUpdater = () => {
  // get the context
  const context = useContext(QLContextUpdater);

  // if `undefined`, throw an error
  if (context === undefined) {
    throw new Error("useQLContextUpdater was used outside of its Provider");
  }

  return context;
};


const QLContextProvider: React.FC = (props) => {
  // the value that will be given to the context
  console.log("QLContest Provider render")

  const emptyState: QLStateType = {
    qList: { questions: [] },
    pdfString: "",
    canBeFilledOnline: true,
    needsToBeSignedInToSubmit: false,
    title: "",
    description: ""
  }

  const [ql, setQl] = useState<QLStateType>(emptyState);

  const myUpdate = (data: QLStateType) => {
    setQl({
      ...data,
      qList: {questions: [...data.qList.questions]}
    })
  }

  const CtxUpdaterDef: QLUpdaterType = {
    qOps: {
      addQuestion: (newq?: Question) => {
        console.log("Adding question in context")
        ql.qList.questions.push(newq)
        myUpdate(ql)
      },

      setQuestion: (q_ind: number, q: Question) => {
        console.log(`Array lens: ${ql.qList.questions.length}`)
        ql.qList.questions[q_ind] = q
        myUpdate(ql)
      },

      delQuestion: (index?: number) => {
        if (index !== undefined && index >= 0 && index < ql.qList.questions.length) {
          for (let i = index; i + 1 < ql.qList.questions.length; ++i) {
            ql.qList.questions[i] = ql.qList.questions[i + 1];
          }
        }
        ql.qList.questions.pop()
        myUpdate(ql)
      }
    },
    sOps: {
      setPdfString: (q: string) => {
        ql.pdfString = q
        myUpdate(ql)
      }
    },
    dOps: {
      setDesc: (d: string) => {
        ql.description = d
        myUpdate(ql)
      },
      setTitle: (t: string) => {
        ql.title = t
        myUpdate(ql)
      },
      setFillOnline: (b: boolean) => {
        ql.canBeFilledOnline = b
        myUpdate(ql)
      },
      setSigndSubmit: (b: boolean) => {
        ql.needsToBeSignedInToSubmit = b
        myUpdate(ql)
      }
    }
  }

  return (
    // the Providers gives access to the context to its children
    <QLContextState.Provider value={ql}>
      <QLContextUpdater.Provider value={CtxUpdaterDef}>
        {props.children}
      </QLContextUpdater.Provider>
    </QLContextState.Provider>
  );
};

export { QLContextProvider, useQLContextState, useQLContextUpdater };
