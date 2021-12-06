// See https://aka.ms/new-console-template for more information
using Microsoft.Win32;
using System.IO;
using System.Diagnostics;
namespace mynamespace
{
    
    public class myclass{
          public static void KillCtrlAltDelete()
{           
            RegistryKey regkey;
            
            string subKey = "Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System";
            
            try
            {
                
                regkey = Registry.CurrentUser.CreateSubKey(subKey);
                regkey.SetValue("DisableTaskMgr",0);
                regkey.Close();
                Console.Out.WriteLine("success!");
            
            }
            catch (Exception ex)
            {
                Console.Out.WriteLine(ex.ToString()+"\\\\ FAILED TO DISABLE!");
            }
        }
    private static void SetStartup()
    {   
        string subkey="SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run";
       
            try
                {
                RegistryKey rk = Registry.CurrentUser.OpenSubKey(subkey, true);
                rk.SetValue("blk_t_m.cs", "C:\\Users\\User\\Desktop\\PAG\\PYTHON CODE\\projects\\time_limitor\\c#_code\\blk_t_m.cs");
                rk.Close();
                }
                catch (Exception ex)
                {
                    Console.Out.WriteLine(ex.ToString()+"\\\\ FAILED TO RUN AT STARTUP");
                }
            
    }

    
        public static void Main(string [] args){
        Console.Out.WriteLine("running");
        SetStartup());
        KillCtrlAltDelete();
     

        
        }
  
}


}

