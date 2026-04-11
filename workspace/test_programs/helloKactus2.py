# import sys
# import os

# sys.path.append("/home/metagen/work/yangjun/kactusdev/build/executable")
# os.environ["LD_LIBRARY_PATH"] = "/home/metagen/work/yangjun/kactusdev/build/executable:" + "/opt/python/3.12/linux/RHEL70/lib/:" + os.environ.get("LD_LIBRARY_PATH", "")

# import pythonAPI as api

def test1(api, lib_path='/home/metagen/work/yangjun/kactusdev/build/executable/Library'):
    kac = api.PythonAPI()
    kac.addLibraryPath(lib_path)
    kac.setDefaultLibraryPath(lib_path)
    kac.setupLibrary(lib_path)

    vender = "tut.fi";lib = "cpu.subsystem";name = "core_example.design";ver = "1.0";vlnv = f"{vender}:{lib}:{name}:{ver}"

    if kac.openDesign(vlnv):
        comps = kac.listComponentsInDesign()
        for comp_name in comps:
            comp_vlnv = kac.getInstanceComponentVLNV(comp_name)
            print(comp_name, comp_vlnv)
        kac.closeOpenDesign()

def test2(api, lib_path='/home/metagen/work/yangjun/kactusdev/build/executable/Library'):
    kac = api.PythonAPI()
    kac.addLibraryPath(lib_path)
    kac.setDefaultLibraryPath(lib_path)
    kac.setupLibrary(lib_path)

    vendor = "test"
    lib = "busdef"
    name = "busdef_example"
    ver = "1.0"
    busdef_vlnv = f"{vendor}:{lib}:{name}:{ver}"

    if kac.createBusDefinition(vendor, lib, name, ver):
        print("Bus definition created successfully.")
    else:
        print("Failed to create bus definition.")

    if kac.createAbstractionDefinition(vendor, lib, name+'.absDef', ver, busdef_vlnv):
        print("Abstraction definition created successfully.")
    else:
        print("Failed to create abstraction definition.")

    kac.createComponent(vendor,"comp","component_example",ver)
    if kac.openComponent(f"{vendor}:comp:component_example:{ver}"):
        p_if = kac.getPortsInterface()
        p_if.addWirePort("data_in")
        p_if.setDirection("data_in", "in")
        p_if.setLeftBound("data_in", "7")
        p_if.setRightBound("data_in", "0")
        p_if.addWirePort("data_out")
        p_if.setDirection("data_out", "out")
        p_if.setLeftBound("data_out", "7")
        p_if.setRightBound("data_out", "0")
        # p_if.setTypeName("data_in", 'logic')
        bus_if_if = kac.getBusInterface()
        bus_if_if.addBusInterface("bus_if_data_in")
        bus_if_if.setBustype("bus_if_data_in", vendor, lib, name, ver)
        bus_if_if.addAbstractionType("bus_if_data_in", vendor,lib,name+'.absDef',ver)
        bus_if_if.setMode("bus_if_data_in", "target")
        bus_if_if.addBusInterface("bus_if_data_out")
        bus_if_if.setBustype("bus_if_data_out", vendor, lib, name, ver)
        bus_if_if.addAbstractionType("bus_if_data_out", vendor,lib,name+'.absDef',ver)
        bus_if_if.setMode("bus_if_data_out", "initiator")
        kac.saveComponent()
        if kac.openAbstractionDefinition(f"{vendor}:{lib}:{name}.absDef:{ver}"):
            abs_if = bus_if_if.getAbstractionTypeInterface()
            pm_if = abs_if.getPortMapInterface()
            lp_if = pm_if.getLogicalPortInterface()
            lp_if.addModeSpecificWireSignal("logical_data_in", "target")
            lp_if.addModeSpecificWireSignal("logical_data_out", "initiator")
            lp_if.setPresence(0, "optional")
            lp_if.setDirection(0, "in")
            lp_if.setPresence(1, "optional")
            lp_if.setDirection(1, "out")
            # print("itemCount:", lp_if.itemCount())
            # print("names:", lp_if.getItemNames())
            # print("mode(0):", lp_if.getModeString(0))
            # print("mode(1):", lp_if.getModeString(1))
            # print(lp_if.getItemNamesWithModeAndGroup("target",""))
            # print(lp_if.getItemNamesWithModeAndGroup("initiator",""))
            kac.saveAbstractionDefinition()
            kac.closeOpenAbstractionDefinition()
        addPortMap(kac, "bus_if_data_in", "logical_data_in", "data_in")
        addPortMap(kac, "bus_if_data_out", "logical_data_out", "data_out")
        kac.saveComponent()
        kac.closeOpenComponent()

def test3(api, lib_path='/home/metagen/work/yangjun/kactusdev/build/executable/Library'):
    kac = api.PythonAPI()
    kac.addLibraryPath(lib_path)
    kac.setDefaultLibraryPath(lib_path)
    kac.setupLibrary(lib_path)

    vendor = "test"
    lib = "busdef"
    name = "busdef_example"
    ver = "1.0"

    if kac.openComponent(f"{vendor}:comp:component_example:{ver}"):
        bus_if_if = kac.getBusInterface()
        bus_if_if.setupSubInterfaces("bus_if_data_in")
        abs_if = bus_if_if.getAbstractionTypeInterface()
        abs_if.setupAbstractionTypeForPortMapInterface(0)
        print("Abstraction types:", abs_if.itemCount())
        print("Abstraction type names:", abs_if.getItemNames())
        pm_if = abs_if.getPortMapInterface()
        print("Port maps:", pm_if.itemCount())
        print("Port map names:", pm_if.getItemNames())
        # lp_if = pm_if.getLogicalPortInterface()
        bus_if_if.setupSubInterfaces("bus_if_data_out")
        abs_if = bus_if_if.getAbstractionTypeInterface()
        abs_if.setupAbstractionTypeForPortMapInterface(0)
        print("Abstraction types:", abs_if.itemCount())
        print("Abstraction type names:", abs_if.getItemNames())
        pm_if = abs_if.getPortMapInterface()
        print("Port maps:", pm_if.itemCount())
        print("Port map names:", pm_if.getItemNames())
        kac.closeOpenComponent()

def addPortMap(kac, bus_if_name, logical_port_name, physical_port_name):
    bus_if_if = kac.getBusInterface()
    bus_if_if.setupSubInterfaces(bus_if_name)
    abs_if = bus_if_if.getAbstractionTypeInterface()
    abs_if.setupAbstractionTypeForPortMapInterface(0)
    pm_if = abs_if.getPortMapInterface()
    row = pm_if.itemCount()
    pm_if.addPortMap(row)
    pm_if.setLogicalPort(row, logical_port_name)
    pm_if.setPhysicalPort(row, physical_port_name)
    # print(pm_if.connectPorts(logical_port_name, physical_port_name))
    print(pm_if.itemCount(), pm_if.getItemNames())
    kac.saveComponent()

def main():
    import pythonAPI
    print('env set!')

if __name__ == '__main__':
    main()