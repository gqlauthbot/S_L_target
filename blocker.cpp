LRESULT CALLBACK LowLevelKeyboardProc(int nCode, WPARAM wParam, LPARAM lParam)
{
if (nCode == HC_ACTION)
{
KBDLLHOOKSTRUCT* p = (KBDLLHOOKSTRUCT*) lParam;
if (p->vkCode == VK_LMENU) // VK_LMENU = ALT key
{
switch (wParam){

case WM_SYSKEYDOWN :{ // use SYSKEYDOWN
cout << "Key down" << endl;

keybd_event(VK_LCONTROL, 0x1D, KEYEVENTF_EXTENDEDKEY | 0, 0 );
break;
}
case WM_KEYUP: // use regular keyup
{
cout << "Key up" << endl;

keybd_event( VK_LCONTROL, 0x1D, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0);
return 1;

break;
}
default:
wParam = WM_SYSKEYDOWN; // if you do not specify it changes back to alt
break;
}
return 1;
}
}
return CallNextHookEx(hHook, nCode, wParam, lParam);
}