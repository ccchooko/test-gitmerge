    @check_attributes(("operator_name", "other_test"))    
    def migrate(self):
        """
        迁移实例
        :return: 执行结果
        :rtype: dict
        """
        if hasattr(self, "target_host") and \
                bns.is_hostname(self.target_host) is False:
            return {
                "status": False,
                "message": "target_host %s is INVALID" % self.target_host
            }
        return self.__migrate(METHOD="migrate")

    @check_attributes(("operator_name"))
    def live_migrate(self):
        """

        :param instance:
        :return:
        """
        nova_driver = nova.Driver(self.cluster)

        res = {"status": False}
        if nova_driver is None:
            res["message"] = "Get cluster for %s failed" % self.name
            return res
            
        vm_attrs = nova_driver.get_instance_attrs(self.uuid)
        hypervisor = vm_attrs.get("hypervisor")
        if hypervisor:
            setattr(self, "hypervisor", hypervisor)

        metainfo_res = nova_driver.get_instance_metainfo(self.name)

        if metainfo_res["status"] is False:
            return metainfo_res

        log.info("meta info type = %s res = %s" % (type(metainfo_res["message"]),
                                                   metainfo_res["message"]))

        for k, v in metainfo_res["message"].items():
            log.info("metainfo %s = %s" % (k, v))
        metainfo = metainfo_res["message"]
        metainfo["src_host"] = self.hypervisor

        if hasattr(self, "target_host"):
            metainfo["dst_host"] = self.target_host

        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        res = self.__migrate(METHOD="live-migration")
        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        if "request_id" in res.keys():
            metainfo["request_id"] = res["request_id"]

        record_res = db_tool.nova_migrate_suc_rate_record(
            cluster=self.cluster, uuid=self.name,
            start_time=start_time, end_time=end_time, metainfo=metainfo,
            migrate_result=0 if res["status"] is True else 1)
        log.info("vm driver migrate record_res = %s" % record_res)
        
        print "hahahahaha"

        return res

    def __migrate(self, METHOD):
        nova_driver = nova.Driver(self.cluster)

        res = {"status": False}
        if nova_driver is None:
            res["message"] = "Get cluster for %s failed" % self.name
            return res
        vm_attrs = nova_driver.get_instance_attrs(self.uuid)
        hypervisor = vm_attrs.get("hypervisor")
        if hypervisor:
            setattr(self, "hypervisor", hypervisor)

        res = nova_driver.migrate(self, METHOD=METHOD)
        return res

    def gagag():
        pass

    @check_attributes(("operator_name"))
    def live_migrate(self):
        pass
