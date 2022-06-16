import React, { ReactNode, useEffect } from "react"

import { createContext, useContext, useState } from "react";
import { GetUserDetails, UserDetails } from "~/api/user/UserDetails";

// TODO: Renamme CoolContext To DynamicListQuestion stuff

interface UserUpdater {
  doUpdate(): void
}

interface UserType {
  authenticated?: boolean
  data?: UserDetails
}

// create contexts
const UserContextState = createContext<undefined | UserType>(undefined);
const UserContextUpdater = createContext<undefined | UserUpdater>(undefined);

// context consumer hook
const useUserState = () => {
  // get the context
  const context = useContext(UserContextState);

  // if `undefined`, throw an error
  if (context === undefined) {
    throw new Error("useUserState was used outside of its Provider");
  }

  return context;
};

// context consumer hook
const useUserUpdater = () => {
  // get the context
  const context = useContext(UserContextUpdater);

  // if `undefined`, throw an error
  if (context === undefined) {
    throw new Error("useUserUpdater was used outside of its Provider");
  }

  return context;
};


const UserContextProvider = (props: {children: ReactNode}) => {
  // the value that will be given to the context
  console.log("UserContextProvider Provider render")

  const notKnown: UserType = {
    authenticated: undefined
  }

  const [user, setUser] = useState<UserType>(notKnown);

  const userUpdater: UserUpdater = {
    doUpdate: async () => {
      console.log("Performing user check")

      const rez = await GetUserDetails()

      console.log("Result from user details: ")
      console.log(rez)

      if (rez === undefined) {
        setUser({
          authenticated: undefined
        })
      } else if (rez.is_signed_in === true) {
        setUser({
          authenticated: true,
          data: rez
        })
      } else {
        setUser({
          authenticated: false
        })
      }
    }
  }

  useEffect(() => {
    userUpdater.doUpdate()
  }, [])

  return (
    // the Providers gives access to the context to its children
    <UserContextState.Provider value={user}>
      <UserContextUpdater.Provider value={userUpdater}>
        {props.children}
      </UserContextUpdater.Provider>
    </UserContextState.Provider>
  );
};

export { UserContextProvider, useUserState, useUserUpdater };
