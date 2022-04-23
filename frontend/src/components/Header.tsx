import { Switch } from "@mui/material"
import React from "react"

interface HeaderProps
{
  themeChanger: React.Dispatch<React.SetStateAction<boolean>>
  isDarkTheme: boolean
}

export default function Header(props: HeaderProps): JSX.Element
{
  const switchClicked = () => {
    const newVal = !props.isDarkTheme
    props.themeChanger(newVal)

    if (newVal)
      localStorage.setItem("isDarkTheme", "true")
    else
      localStorage.setItem("isDarkTheme", "false")
  }

  return <>
    <Switch checked={props.isDarkTheme} onChange={switchClicked} />
  </>
}
