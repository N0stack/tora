# coding:utf-8
import operation.pool as Poolop
from info.pool import PoolInfo
from resource.util import abort_if_poolname_doesnot_exist, abort_if_poolname_exists
from flask_restful import Resource, reqparse


class Pool(Resource):
    def get(self):
        """
        get all pool info
        """
        poolinfo = PoolInfo()

        return poolinfo.get_pool_info_all(), 200


class Poolname(Resource):
    def get(self, name):
        """
        get pool info
        """
        poolinfo = PoolInfo()
        abort_if_poolname_doesnot_exist(name)
        return poolinfo.get_pool_info(), 200

    def post(self, name):
        """
        create pool
        """
        # check pool name
        abort_if_poolname_exists(name)

        # set parser
        parser = reqparse.RequestParser()
        parser.add_argument('pool_path', type=str, location='json', required=False)

        args = parser.parse_args()
        poolcreate = Poolop.Create()

        if 'pool_path' in args.keys():
            is_success = poolcreate(pool_name=name, pool_path=args['pool_path'])
            if is_success is False:
                return {"message": "failed"}, 400
            else:
                return {"message": "successful"}, 201
        else:
            is_success = poolcreate(pool_name=name)
            if is_success is False:
                return {"message": "failed"}, 400
            else:
                return {"message": "successful"}, 201
            
    def delete(self, name):
        """
        delete pool
        """
        # check pool name
        abort_if_poolname_doesnot_exist(name)

        pooldelete = Poolop.Delete()
        is_success = pooldelete(name)

        if is_success is False:
            return {"message": "failed"}, 400
        else:
            return {"message": "successful"}, 201
