#!/usr/bin/python
# -*- coding: utf8 -*-

from lib.BdpSDK import BdpSDK
import copy


class TFolder(object):

    @classmethod
    def get_all_folder_list(cls, force=True):

        if not force:
            return
        else:
            return cls.refresh_all_folder_list()

    @classmethod
    def refresh_all_folder_list(cls):
        def _get_forlders(old_folders):
            assert isinstance(old_folders, list)
            new_folders = copy.deepcopy(old_folders)
            for old_folder in old_folders:
                if "sub_folders" in old_folder and old_folder["sub_folders"]:
                    new_folders.extend(_get_forlders(old_folder["sub_folders"]))

            return new_folders

        bdp = BdpSDK.instance()
        folders = bdp.call_method_and_succ("folder_list", ret_expr='["result"]')

        return _get_forlders(folders)

    @classmethod
    def get_folder_tree(cls):
        def _get_forlders(old_folders):
            assert isinstance(old_folders, list)
            new_folders = copy.deepcopy(old_folders)
            for old_folder in old_folders:
                if "sub_folders" in old_folder and old_folder["sub_folders"]:
                    new_folders.extend(_get_forlders(old_folder["sub_folders"]))

            return new_folders

        def _get_forlder_tbs(old_folders):
            assert isinstance(old_folders, list)
            new_folders = copy.deepcopy(old_folders)
            index = 0
            for folder in new_folders:
                tb_list = bdp.call_method_and_succ("folder_tb_list", folder['folder_id'], ret_expr='["result"]')
                new_folders[index]["tb_list"] = tb_list
                index += 1
            return new_folders

        bdp = BdpSDK.instance()
        folders = bdp.call_method_and_succ("folder_tree", ret_expr='["result"]["folder_list"]')

        return _get_forlder_tbs(_get_forlders(folders))

    def __init__(self):
        self.folder_id = ""
        self._name = ""
        self._parent_id = None
        self.tbs = []
        self.seq_no = ""
        self.bdp = BdpSDK.instance()
        self._sub_folders = []

    def name(self):
        return self._name

    def seqnumber(self):
        return self.seq_no

    def id(self):
        return self.folder_id

    def parent_id(self):
        return self._parent_id

    def refresh(self):
        _folders = TFolder.refresh_all_folder_list()
        for f in _folders:
            if f["folder_id"] == self.folder_id:
                self.tbs = f["tb_list"] if "tb_list" in f else []
                self._name = f["name"]
                self.seq_no = f["seq_no"]
                if "parent_id" in f:
                    self._parent_id = f["parent_id"]
                else:
                    self._parent_id = None

                if "sub_folders" in f and f["sub_folders"]:
                    self._sub_folders = f["sub_folders"]
                else:
                    self._sub_folders = []

                break

    def table_list(self):
        return self.tbs

    def table_ids(self):
        return [t["tb_id"] for t in self.tbs]

    def sub_folder_ids(self):
        return [f["folder_id"] for f in self._sub_folders]

    def sub_folder_names(self):
        return [f["name"] for f in self._sub_folders]

    @classmethod
    def _from_folder_id_or_name(cls, folder_id=None, name=None, _folders=None):

        if not _folders:
            _folders = cls.refresh_all_folder_list()
        for f in _folders:
            if f["folder_id"] == folder_id or f["name"] == name:
                folder = TFolder()
                folder.folder_id = f["folder_id"]
                folder._name = f["name"]
                folder.tbs = f["tb_list"] if "tb_list" in f else []
                folder.seq_no = f["seq_no"]

                if "parent_id" in f:
                    folder._parent_id = f["parent_id"]
                else:
                    folder._parent_id = None

                if "sub_folders" in f and f["sub_folders"]:
                    folder._sub_folders = f["sub_folders"]
                else:
                    folder._sub_folders = []

                return folder

        return None

    @classmethod
    def from_folderid(cls, folder_id, _folders=None):
        return cls._from_folder_id_or_name(folder_id=folder_id, _folders=_folders)

    @classmethod
    def from_foldername(cls, name, _folders=None):

        real_name = "" if name == "/" else name

        return cls._from_folder_id_or_name(name=real_name, _folders=_folders)

    @classmethod
    def create(cls, name, parent_folder="/"):

        if isinstance(parent_folder, TFolder):
            p_folder = parent_folder

        else:
            p_folder = TFolder.from_foldername(parent_folder)

        assert p_folder is not None

        # 子文件夹不能创建文件夹, 暂时设计为这样
        assert p_folder.parent_id() in ("", None)

        bdp = BdpSDK.instance()

        folder_id = bdp.call_method_and_succ("folder_create", name, p_folder.folder_id, ret_expr='["result"]["folder"]')

        return cls.from_folderid(folder_id)

    def move_to(self, parent_folder="/"):

        if isinstance(parent_folder, TFolder):
            p_folder = parent_folder

        else:
            p_folder = TFolder.from_foldername(parent_folder)

        # 根目录不能移动
        assert self.folder_id != "folder_root"

        # 目标目录未找到
        assert p_folder is not None

        # 不能移动至子文件夹, 前端限制, 后端是否有限制?
        if p_folder.parent_id() or (p_folder.parent_id() == "" and self._sub_folders):
            print "can not move to sub folder"
            assert False

        self.bdp.call_method_and_succ("folder_modifyparent", self.folder_id, p_folder.folder_id, self.seq_no)

        self.refresh()

    def rename(self, name):

        self.bdp.call_method_and_succ("folder_modify", self.folder_id, name)

        self.refresh()

    def delete(self, delete_mode=0):

        self.bdp.call_method_and_succ("folder_delete", self.folder_id, delete_mode)

    def top(self, seq=0):
        self.bdp.call_method_and_succ("folder_modifyseq", self.folder_id, seq)
        self.refresh()

    def batch_move(self, tb_ids):
        change_list = []
        for tb_id in tb_ids:
            change_list.append({"tb_index": 0, "tb_id": tb_id})

        self.bdp.call_method_and_succ("folder_batch_change", change_list, self.folder_id)
        self.refresh()
