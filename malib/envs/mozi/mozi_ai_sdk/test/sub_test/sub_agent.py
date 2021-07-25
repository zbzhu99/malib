# _*_ coding : utf-8 _*_
'''
作者 : 解洋
时间: 2020-3-25
'''
# _*_ coding : utf-8 _*_
'''
作者 : 解洋
时间: 2020-3-24
'''

class CAgent():
    def __init__(self):
        self.class_name = 'aircraft_'
    def test(self,scenario):
        for side_k , side_v in scenario.get_sides().items():
            if len(side_v.submarines) > 0:
                #测试潜艇
                print(5)
                for sub_k , sub_v in side_v.submarines.items():
                    print('mount:')
                    print(sub_v.get_mounts())
                    print('senaor')
                    print(sub_v.get_sensor())
                    print('magazine')
                    print(sub_v.get_magazines())
                    print('doctine')
                    print(sub_v.get_doctrine())
                    print('# 对象类名')
                    print(sub_v.ClassName)
                    print('# 名称')
                    print(sub_v.strName)
                    print('# Guid')
                    print(sub_v.strGuid)
                    print('# 地理高度')
                    print(sub_v.fAltitude_AGL)
                    print('# 海拔高度')
                    print(sub_v.iAltitude_ASL)
                    print('# 所在推演方ID')
                    print(sub_v.m_Side)
                    print('# 单元类别')
                    print(sub_v.strUnitClass)
                    print('# 当前纬度')
                    print(sub_v.dLatitude)
                    print('# 当前经度')
                    print(sub_v.dLongitude)
                    print('# 当前朝向')
                    print(sub_v.fCurrentHeading)
                    print('# 当前速度')
                    print(sub_v.fCurrentSpeed)
                    print('# 当前海拔高度')
                    print(sub_v.fCurrentAltitude_ASL)
                    print('# 倾斜角')
                    print(sub_v.fPitch)
                    print('# 翻转角')
                    print(sub_v.fRoll)
                    print('# 获取期望速度')
                    print(sub_v.fDesiredSpeed)
                    print('# 获取最大油门')
                    print(sub_v.m_MaxThrottle)
                    print('# 最大速度')
                    print(sub_v.fMaxSpeed)
                    print('# 最小速度')
                    print(sub_v.fMinSpeed)
                    print('# 当前高度')
                    print(sub_v.fCurrentAlt)
                    print('# 期望高度')
                    print(sub_v.fDesiredAlt)
                    print('# 最大高度')
                    print(sub_v.fMaxAltitude)
                    print('# 最小高度')
                    print(sub_v.fMinAltitude)
                    print('# 军标ID')
                    print(sub_v.strIconType)
                    print('# 普通军标')
                    print(sub_v.strCommonIcon)
                    print('# 数据库ID')
                    print(sub_v.iDBID)
                    print('# 是否可操作')
                    print(sub_v.bIsOperating)
                    print('# 编组ID')
                    print(sub_v.m_ParentGroup)
                    print('# 停靠的设施的ID(关系)')
                    print(sub_v.m_DockedUnits)
                    print('# 单元的停靠设施(部件)')
                    print(sub_v.m_DockFacilitiesComponent)
                    print('# 停靠的飞机的ID(关系)')
                    print(sub_v.m_DockAircrafts)
                    print('# 单元的航空设施(部件)')
                    print(sub_v.m_AirFacilitiesComponent)
                    print('# 单元的通信设备及数据链(部件)')
                    print(sub_v.m_CommDevices)
                    print('# 单元的引擎(部件')
                    print(sub_v.m_Engines)
                    print('# 传感器，需要构建对象类,所以只传ID')
                    print(sub_v.m_Sensors)
                    print('# 挂架')
                    print(sub_v.m_Mounts)
                    print('# 毁伤状态')
                    print(sub_v.strDamageState)
                    print('# 失火')
                    print(sub_v.iFireIntensityLevel)
                    print('# 进水')
                    print(sub_v.iFloodingIntensityLevel)
                    print('# 分配的任务')
                    print(sub_v.m_AssignedMission)
                    print('# 作战条令')
                    print(sub_v.m_Doctrine)
                    print('# 系统右栏->对象信息->作战单元武器')
                    print(sub_v.m_UnitWeapons)
                    print('# 路径点')
                    print(sub_v.m_WayPoints)
                    print('# 训练水平')
                    print(sub_v.m_ProficiencyLevel)
                    print('# 是否是护卫角色')
                    print(sub_v.bIsEscortRole)
                    print('# 当前油门')
                    print(sub_v.m_CurrentThrottle)
                    print('# 通讯设备是否断开')
                    print(sub_v.bIsCommsOnLine)
                    print(sub_v.bIsIsolatedPOVObject)
                    print('# 地形跟随')
                    print(sub_v.bTerrainFollowing)
                    print(sub_v.bIsRegroupNeeded)
                    print('# 保持阵位')
                    print(sub_v.bHoldPosition)
                    print('# 是否可自动探测')
                    print(sub_v.bAutoDetectable)
                    print('# 当前货物')
                    print(sub_v.m_Cargo)
                    print('# 燃油百分比，作战单元燃油栏第一个进度条的值')
                    print(sub_v.dFuelPercentage)
                    print('# 获取AI对象的目标集合# 获取活动单元AI对象的每个目标对应显示不同的颜色集合')
                    print(sub_v.m_AITargets)
                    print('# 获取活动单元AI对象的每个目标对应显示不同的颜色集合')
                    print(sub_v.m_AITargetsCanFiretheTargetByWCSAndWeaponQty)
                    print('# 获取单元的通讯链集合')
                    print(sub_v.m_CommLink)
                    print('# 获取传感器0')
                    print(sub_v.m_NoneMCMSensors)
                    print('# 获取显示"干扰"或"被干扰"')
                    print(sub_v.iDisturbState)
                    print('# 单元所属多个任务数量')
                    print(sub_v.iMultipleMissionCount)
                    print('# 单元所属多个任务guid拼接')
                    print(sub_v.m_MultipleMissionGUIDs)
                    print('# 是否遵守电磁管控')
                    print(sub_v.bObeysEMCON)
                    print('# 武器预设的打击航线')
                    print(sub_v.m_strContactWeaponWayGuid)
                    print('# 停靠参数是否包含码头')
                    print(sub_v.bDockingOpsHasPier)
                    print('弹药库')
                    print(sub_v.m_Magazines)
                    print('被摧毁')
                    print(sub_v.dPBComponentsDestroyedWidth)
                    print("轻度")
                    print(sub_v.dPBComponentsLightDamageWidth)
                    print('# 中度')
                    print(sub_v.dPBComponentsMediumDamageWidth)
                    print('''# 重度''')
                    print(sub_v.dPBComponentsHeavyDamageWidth)
                    print('''# 重度''')
                    print(sub_v.dPBComponentsHeavyDamageWidth)
                    print('''# 正常''')
                    print(sub_v.dPBComponentsOKWidth)
                    print('''# 配属基地''')
                    print(sub_v.m_HostActiveUnit)
                    print(''' # 状态''')
                    print(sub_v.strActiveUnitStatus)
                    print('''# 精简''')
                    print(sub_v.doctrine)

                    side_v.add_mission_strike('打击任务', 0)
                    for contact_k, contact_v in side_v.contacts.items():
                        sub_v.auto_attack(contact_k)
                        sub_v.manual_attack(contact_k, 20, 1)
                        break
                    sub_v.set_throttle(2)
                    sub_v.set_radar_shutdown('true')
                    sub_v.set_desired_height(3000)
                    sub_v.return_to_base()
                    sub_v.assign_unitlist_to_mission('打击任务')
                    sub_v.cancel_assign_unitlist_to_mission()
                    sub_v.plot_course([(40, -39.0)])
                    sub_v.assign_unitlist_to_mission_escort('打击任务')
            scenario.mozi_server.run_simulate()
            # self.mozi_server.run_simulate()
            # self.mozi_server.run_simulate()